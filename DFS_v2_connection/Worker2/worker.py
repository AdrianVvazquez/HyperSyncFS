import rpyc 
import os
from os import listdir
from os.path import isfile, join

@rpyc.service
class WorkerService(rpyc.Service):
    ALIASES = ["SUPER_WORKER", 'WORKER2']
    ip = ('localhost', 18862)
    auth_key = ''
    
    @rpyc.exposed
    def put_chunk(self, chunk, directoryIndex):
        dir_name = f"{chunk['file_name']}"
        file_name = f"{chunk['index']}-{chunk['chunk_id']}"
        os.makedirs(dir_name, exist_ok=True)
        
        with open(f"{dir_name}/{file_name}", 'wb') as f:
            f.write(chunk['data'])

    @rpyc.exposed
    def get_chunk_2(self, chunk):
        chunk_name = f"{chunk['file_name']}/{chunk['index']}-{chunk['chunk_id']}"
        with open(chunk_name, 'rb') as f:
            return f.read()
    
    @rpyc.exposed
    def get_chunk(self, chunk, write_to_client):
        chunk_name = f"{chunk['file_name']}/{chunk['index']}-{chunk['chunk_id']}"
        with open(chunk_name, 'r') as f:
            cache_file = write_to_client(chunk['file_name'], f.read())
        return cache_file

def authenticate(master, user_name, ip, port):
    print(f"\nBIENVENIDO {user_name}")
    try:
        with open('auth.txt', 'r') as f:
            # Autenticar por user_name
            credentials = [line.strip().split('/') for line in f if user_name in line]
            if credentials:
                _, key = credentials[0]
                master.Auth_Host(user_name, ip, port, key)
                print("#"*50)
                print('Mi id: ', key)
                print("#"*50, '\n')
                return key
            else:
                print("[Error]: No estás registrado.")
                # TODO: ¿registrarse?
                
    
    except FileNotFoundError:
        # Crear archivo de autenticación
        with open("auth.txt", "w") as f:
            key = master.Auth_Host(user_name, ip, port)
            f.write(user_name+'/'+key)
            print("#"*50)
            print(f'Tu usuario para server auth: {user_name}')
            print(f'ID generado en auth.txt: {key} para server auth')
            print("#"*50, '\n')
            return key

    except ValueError:
        print("[Auth Error]: Borra el archivo auth.txt y vuelve a correr el programa.")


def Connect_to_Master(service):
    print("connecting to Master")
    conn = rpyc.connect('localhost', 18861, service=service)
    # get key
    user_name = service.get_service_aliases()[1]
    key = authenticate(conn.root, user_name, service.ip[0], service.ip[1])
    # register as worker
    conn.root.Add_Worker(user_name, key)
    service.host_id = key


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer

    service = WorkerService()
    Connect_to_Master(service)
    t = ThreadedServer(service, port=service.ip[1])
    t.start()

