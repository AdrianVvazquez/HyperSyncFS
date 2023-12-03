import os
import rpyc
import uuid
import math

@rpyc.service
class WorkerService(rpyc.Service):
    ALIASES = ["SUPER_WORKER"]
    My_files = []   # Lista con nombres de los archivos
    Chunks = {}
    Partitions = []

    def __init__(self, worker_id):
        self.worker_id = worker_id
    
    def on_connect(self, conn):
        print(f"[Conexión nueva] {conn}")
        self._conn = conn
        # code that runs when a connection is created
    
    def on_disconnect(self, conn):
        print("[logout]", conn)
        # code that runs after the connection has already closed
        return "¡Adios!"
    
    @rpyc.exposed
    def Share_my_id(self):
        print("sharing id")
        return self.worker_id

    @rpyc.exposed
    def exposed_get_files(self): # this is an exposed method
        return self.My_files
    
    @rpyc.exposed
    def save_chunks(self, chunks): # this is an exposed method
        for chunk in chunks:
            with open(f'{chunk[0]}-{chunk[1]}', 'wb') as f:
                f.write(chunk[3]) 
                print(chunk[1])

        return True

my_port = 18863
my_ip = 'localhost'
if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    from rpyc.utils.helpers import classpartial
    os.path.join

    # Conectarse a Master
    master = rpyc.connect('localhost', 18861)
    serviceMaster = master.root
    

    host_id = serviceMaster.Add_Host('WORKER1', my_ip, my_port)
    serviceMaster.Add_Worker(host_id)
    master.close()
    print("host_id", host_id)
    

    service = classpartial(WorkerService, worker_id=host_id)
    t = ThreadedServer(service, port=my_port)
    t.start()
