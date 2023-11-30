import os
import rpyc
import uuid
import math
import datetime

class File_Metadata():
    def __init__(self, id=None, name=None, owner=None, size=None):
        self.id = id
        self.name = name
        self.size = size
        self.created = datetime.datetime.now()
        self.last_edited = datetime.datetime.now()
        self.permissions = {}  # {user_id: '---', ...}
        self.owner = owner
        self.chunks = []

    def set_chunks(self, chunks):
        self.chunks = chunks

    def get_chunks(self):
        return self.chunks

class Host():
    def __init__(self, id, name, ip ,port):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.My_files = []

    def __str__(self):
        return self.name

CHUNK_SIZE = 100
class MasterService(rpyc.Service):
    registered_hosts = []
    active_connections = []  
    Chunks = []     # [ (uuid, index, worker_id, data), ... ]
    Workers = {}    # { 'id': (ip, port), ... }
    My_files = {}   # { 'file1.txt': { File _Metadata }, ... }

    def on_connect(self, conn):
        self.active_connections.append(conn)
        print(f"[new login]", conn)
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        self.active_connections.remove(conn)
        print(f"[logout]", conn)


    def exposed_Add_Host(self, host_name, host_ip, host_port):
        host = Host(str(uuid.uuid4()), host_name, host_ip, host_port)
        # TODO: si ya existe
        # for host_tmp in self.registered_hosts:
        #     if host_tmp.id == host.id:
        #         print()
        self.registered_hosts.append(host)
        print(self.registered_hosts)
        return host.id


    def exposed_Add_Worker(self, host_id):
        host = [host for host in self.registered_hosts if host_id == host.id][0]
        self.Workers[host.id] = host
        print('[new worker]', host.id, host.name, host.ip, host.port)
        return True


    def exposed_read(self, user_id, file_name):
        file_tmp = self.My_files.get(file_name)

        if not file_tmp:
            return ['err', 'No existe el archivo que buscas.']        
        if file_tmp.owner != user_id:
           return ['err', 'No eres el dueño de este archivo.']
        
        return file_tmp.get_chunks()  # returns a List
        

    def exposed_write(self, file_name, size, data, user_id):  # recv data in binary
        if not self.Workers:
            return "Lo siento. El servicio no está disponible."
        
        # if os.path.exists(f'{file_name.split(".")[0]}-cache.txt'):
        # si archivo ya existe
        if file_name in self.My_files:
            return ['err', 'El archivo que tratas de guardar ya existe. Cambiar el nombre e intenta de nuevo.']

        with open(f'cache/{file_name.split(".")[0]}-cache.txt', 'wb') as f:
            f.write(data)
        
        # save metadata
        md_file = File_Metadata(id=str(uuid.uuid4()), name=file_name, owner=user_id, size=size)

        # get blocks number
        n_blocks = math.ceil(size/CHUNK_SIZE)
        n_packets = math.ceil(n_blocks/len(self.Workers))
        print('...blocks:', n_blocks, 'packets:', n_packets, '...workers:', len(self.Workers))
        
        # Write in workers
        data_seek = 0
        chunk_index = 0
        chunks = []
        for worker_id, worker in self.Workers.items():
            chunks_recv, chunk_index, data_seek = self.Generate_Chunks(data, worker_id, n_packets, chunk_index, data_seek)
            
            conn = rpyc.connect(worker.ip, worker.port)
            conn.root.save_chunks(chunks_recv)  # send chunks to Worker
            chunks.extend(chunks_recv)
            
        md_file.set_chunks(chunks)
        # make copies
        # ...
        self.My_files[file_name] = md_file
        print("¡Archivo creado exitosamente!")
        return md_file.id


    def Generate_Chunks(self, data, worker_id, n_packets, chunk_index, data_seek):
        chunks = []
        for p in range(n_packets):
            chunk_id = str(uuid.uuid4())  # chunk ID
            data_tmp = data[data_seek: data_seek+ CHUNK_SIZE]
            chunks.append((chunk_id, chunk_index+1, worker_id, data_tmp))
            chunk_index+= 1
            data_seek+= CHUNK_SIZE
        return chunks, chunk_index, data_seek

        
# TODO: 
# from rpyc.utils.authenticators import AuthenticationError
# def magic_word_authenticator(sock):
#     if sock.recv(5) != "Ma6ik":
#         raise AuthenticationError("wrong magic word")
#     return sock, None

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    os.path.join
    # run service
    t = ThreadedServer(MasterService(), port=18861)
    #     'allow_public_attrs': True,
    # })
    # }, authenticator = magic_word_authenticator)
    t.start()
