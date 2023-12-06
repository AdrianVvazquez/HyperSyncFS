import os
import rpyc
import uuid
import math
from datetime import datetime
import json
import hashlib

CHUNK_SIZE = 100

class File():
    data_seek = 0
    chunk_index = 0
    worker_index = 0
    chunks_number = 0
    chunks_perWorker = 0
    chunk_size = CHUNK_SIZE


    def __init__(self, id=None, name=None, owner=None, size=None):
        self.id = id
        self.name = name
        self.size = size
        self.created = datetime.now()
        self.last_edited = datetime.now()
        self.permissions = {}  # {user_id: '---', ...} qué usuarios tienen permiso sobre este archivo
        self.owner = owner
        self.chunks = [] # [{index, file_name, chunk_id, worker_id}, ...]
        self.hash_generator = hashlib.sha256()

    def reset_chunk_index(self):
        self.data_seek = 0
        self.chunk_index = 0

    def set_chunks(self, chunks):
        self.chunks = chunks

    def save_chunk(self, chunk):
        self.chunks.append(chunk)

    def get_chunks(self):
        return self.chunks

    def get_chunks_number(self):
        self.chunks_number = math.ceil(self.size/self.chunk_size)

    def get_chunks_perWorker(self, Workers_length):
        self.chunks_perWorker = math.ceil(self.chunks_number/Workers_length)
    
    def save_metadata(self, md_file):
        obj = {
            'created':str(self.created),
            'id':str(self.id),
            'last_edited':str(self.last_edited),
            'name':str(self.name),
            'owner':str(self.owner),
            'permissions':self.permissions,
            'size':str(self.size),
            'sha256':str(self.hash_generator.hexdigest()),
            'chunks':self.chunks,
        }
        with open(md_file, 'r+') as f:
            if not f.read(1):
                lista = []
            else:
                f.seek(0)
                lista = json.load(f)
            lista.append(obj)   # leer lista y añadir objeto 
            f.seek(0)
            json.dump(lista, f, indent=4) # escribir lista actualizada
        

class Host():
    def __init__(self, id, name, ip ,port):
        self.id = id
        self.name = name
        self.auth = None
        self.ip = ip
        self.port = port
        self.My_files = {}  # { 'file1.txt': File, ... }

    def __str__(self):
        return self.name
    
    def Authenticate(self, auth_key):
        self.auth = auth_key


@rpyc.service
class MasterService(rpyc.Service):
    registered_hosts = {}   # {username: Host, ...}
    active_connections = []  
    Workers = {}    # { 'id': Host, ... }
    My_files = {}   # { 'file1.txt': File, ... }
    md_file = 'cache-metadata/saved-files.json'
    Ready = False
    chunk_size = CHUNK_SIZE

    def init_data(self):
        # bring caché to memory 
        try:
            with open(self.md_file, 'r') as  f:
                data = f.read()
                if not data:
                    print("No hay datos todavía.")
                    self.ready = True
                    return 
                
                # load metadata list
                f_list = json.loads(data)
                for file in f_list:
                    # create new File instance
                    file_obj = File(id=file['id'], name=file['name'], owner=file['owner'], size=file['size'])
                    file_obj.created = datetime.fromisoformat(file['created'])
                    file_obj.last_edited = file['last_edited']
                    # set chunks to File
                    file_obj.set_chunks(file['chunks'])
                    # save File instance in My_files diccionary
                    self.My_files.update({file['name']: file_obj})

        except FileNotFoundError:
            # Create cache file if not exist
            print("No existe archivo para escribir, creando uno...")
            os.makedirs(self.md_file.split('/')[0], exist_ok=True)
            f = open(self.md_file, 'x')
            f.close()

        # Master ready
        finally:
            self.ready = True

    def on_connect(self, conn):
        # TODO: Filtrar por service_name los workers y clientes
        # print("[login]", conn.root.get_service_name(), conn.root.get_ip())
        # print("[login]", conn.root.get_service_name(), conn)
        self.active_connections.append(conn)
        # No empezar servicio sin Workers
        if not self.Ready and conn.root.get_service_name() == 'SUPER_WORKER':
            self.init_data()
            
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        print("[logout]", conn)
        self.active_connections.remove(conn)

    @rpyc.exposed
    def Auth_Host(self, user_name, host_ip, host_port, auth_key=None):
        if not auth_key:
            auth_key = str(uuid.uuid4())
        
        if not self.registered_hosts.get(user_name):
            # crear usuario y guardar
            host = Host(auth_key, user_name, host_ip, host_port)
            host.Authenticate(auth_key)
            print('[HOST]:', host)
            self.registered_hosts.update({user_name: host})
            return host.id
        return 'Este usuario ya existe'

    @rpyc.exposed
    def Add_Worker(self, user_name, auth_key):
        # autenticar Workers con nombre y id
        host = self.registered_hosts.get(user_name)
        print("[WORKER]:", host)
        if host and host.id == auth_key:
            self.Workers.update({host.id: host})
            print('[new worker]', host.id, host.name, host.ip, host.port)
            return True

    @rpyc.exposed
    def read(self, userName, file_name, client_write_access):
        if not self.Workers:
            return ['err', "Lo siento. El servicio no está disponible."]
        
        file_tmp = self.My_files.get(file_name)
        # exceptions
        if not file_tmp:
            return ['err', 'No existe el archivo que buscas.']        
        if file_tmp.owner != userName:
           return ['err', 'No eres el dueño de este archivo.'] # return a List
        
        # get chunks reference 
        chunks = file_tmp.get_chunks()
        # get chunks from workers
        data_chunks = []
        for chunk in chunks:
            worker = self.Workers.get(chunk['worker_id'])
            conn = rpyc.connect(worker.ip, worker.port)
            # cache_client_file = conn.root.get_chunk(chunk, client_write_access)
            data_chunks.append(conn.root.get_chunk(chunk))
        client_write_access(file_name, data_chunks)
        
    @rpyc.exposed
    def write(self, file_name, file_size, userName):
        # exceptions
        if not self.Workers:
            return ['err', "Lo siento. El servicio no está disponible."]
        user = self.registered_hosts.get(userName)
        if not user.auth:
            return ['err', "No estás registrado."]
        if file_name in self.My_files:
            return ['err', "El archivo que tratas de guardar ya existe. Cambiar el nombre e intenta de nuevo."]
        
        # create file instance
        new_file = File(id=str(uuid.uuid4()), name=file_name, owner=userName, size=file_size)
        # get blocks number
        new_file.get_chunks_number()
        new_file.get_chunks_perWorker(len(self.Workers))
        user.My_files.update({file_name: new_file})
        self.My_files.update({file_name: new_file})
        print('size...', new_file.size, '...chunks:', new_file.chunks_number, '...workers:', len(self.Workers), '...chunks per worker:', new_file.chunks_perWorker)

        return [self.send_chunk, [new_file.chunks_number, self.chunk_size]]

    def send_chunk(self, file_name, data):
        if len(data) > self.chunk_size:
            return ['err', "Reduce el tamaño de los datos"]
        
        file = self.My_files.get(file_name)
        # select worker
        if file.chunk_index>1 and file.chunk_index%file.chunks_perWorker==0:
            file.worker_index += 1
        worker = list(self.Workers.values())[file.worker_index]
        
        # create chunk
        chunk_id = str(uuid.uuid4())
        chunk_obj = {
            "chunk_id": chunk_id,
            "data": data,
            "file_name": file.name,
            "index": file.chunk_index+1,
            "worker_id": worker.id
        }
        # send chunk to Worker
        conn = rpyc.connect(worker.ip, worker.port)
        conn.root.put_chunk(chunk_obj, file.worker_index)
        # remove data from chunk to save in Master
        chunk_obj.pop("data")
        file.hash_generator.update(data)
        file.save_chunk(chunk_obj)
        # increment chunk counter
        file.chunk_index += 1
        # if all data was send
        if file.chunk_index == file.chunks_number:
            self.My_files.update({file_name: file})
            file.save_metadata(self.md_file)
            return ['ok','¡Archivo creado exitosamente!']
        # make copies
        # ...


# TODO: 
# from rpyc.utils.authenticators import AuthenticationError
# def magic_word_authenticator(sock):
#     if sock.recv(5) != "Ma6ik":
#         raise AuthenticationError("wrong magic word")
#     return sock, None
# authenticator = magic_word_authenticator

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    os.path.join
    # run service
    t = ThreadedServer(MasterService(), port=18861)
    t.start()
