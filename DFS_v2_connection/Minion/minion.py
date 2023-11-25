import os
import rpyc
import uuid
import math

# Generate a random UUID
CHUNKS_SIZE = 100
class Minion(rpyc.Service):
    Connections = []
    My_files = []   # Lista con nombres de los archivos
                    # se puede acceder a él mediante el nombre de la clase o el nombre de una instancia de la clase.
    # my_new_files = self.show_files()

    def __init__(self):
        self.Chunks = {}
        self.Partitions = []

    def on_connect(self, conn):
        print(f"[Conexión nueva] {conn}")
        self.Connections.append(conn)
        # code that runs when a connection is created
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        return "¡Adios!"

    def exposed_get_files(self): # this is an exposed method
        return self.My_files

    def save_chunks(self, chunks): # this is an exposed method
        print(chunks)
        # return self.My_files


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Minion, port=18862, protocol_config={
        'allow_public_attrs': True,
    })
    t.start()
