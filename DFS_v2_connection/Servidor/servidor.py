import os
import rpyc
import json
import uuid

# Generate a random UUID
CHUNKS_SIZE = 100
MY_FILES = []
class DfsService(rpyc.Service):
    exposed_connections = {}
    exposed_files = {}
    chunks_size = CHUNKS_SIZE

    def __init__(self):
    #     self.connections = []
        self.new_files = []

    def on_connect(self, conn):
        print(f"[Conexión nueva] {conn}")
        # code that runs when a connection is created

    # def exposed_listdir(self, d):
    #     return os.listdir(d)
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        return "¡Adios!"

    def exposed_get_files(self): # this is an exposed method
        return self.new_files

    def exposed_write(self, file_name, size, data): # this is an exposed method
        print({
            "put": file_name,
            "size": size,
            "data": data
        })
        # get blocks
        blocks = self.get_blocks(file_name, data)
        with open(file_name, 'wb') as f:
            f.write(data)
            self.new_files.append(f.name)

        print("¡Archivo creado exitosamente!")
        return True
    
    def get_blocks(self, file, data):
        # Write in local
        # random_uuid = uuid.uuid4()

        pass


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(DfsService, port=18861, protocol_config={
        'allow_public_attrs': True,
    })
    t.start()
