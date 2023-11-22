import os
import rpyc

MY_FILES = []
class DfsService(rpyc.Service):
    def __init__(self):
        self.connections = []
        self.new_files = []

    def on_connect(self, conn):
        print(f"[Conexión nueva] {conn}")
        # code that runs when a connection is created
        # (to init the service, if needed)
        self.connections.append(conn)

    def exposed_listdir(self, d):
        return os.listdir(d)
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        return "¡Adios!"

    def exposed_get_files(self): # this is an exposed method
        return self.new_files

    def exposed_create_file(self, new_file): # this is an exposed method
        self.new_files.append(new_file)
        return "¡Archivo creado exitosamente!"

    # exposed_the_real_answer_though = 43 # an exposed attribute

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(DfsService(), port=18861)
    t.start()
