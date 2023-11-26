import os
import rpyc
import uuid
import math

class Minion(rpyc.Service):
    My_files = []   # Lista con nombres de los archivos
    Chunks = {}
    Partitions = []
    
    def on_connect(self, conn):
        print(f"[Conexión nueva] {conn}")
        # code that runs when a connection is created
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        return "¡Adios!"

    def exposed_get_files(self): # this is an exposed method
        return self.My_files

    def Connect_to_Master(self, chunks): # this is an exposed method
        print(chunks)
        # return self.My_files


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    # Conectarse a Master
    remoteMaster = rpyc.connect('localhost', 18861)
    serviceMaster = remoteMaster.root
    minion_id = serviceMaster.Add_Minion()
    print(minion_id)

    t = ThreadedServer(Minion, port=18862, protocol_config={
        'allow_public_attrs': True,
    })
    t.start()
