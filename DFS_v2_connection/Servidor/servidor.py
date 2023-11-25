import os
import rpyc
import uuid
import math

# Generate a random UUID
CHUNKS_SIZE = 100
class DfsService(rpyc.Service):
    Connections = []
    My_files = []   # Lista con nombres de los archivos
                    # se puede acceder a él mediante el nombre de la clase o el nombre de una instancia de la clase.
    # my_new_files = self.show_files()

    def __init__(self):
        self.Chunks = {}
        self.Partitions = []
        self.Minions = []   # [{'ip': [uuid1, uuid2, ...]}, ...]

    # def list_dir(self, dir): 
    #     return os.listdir(dir)

    def on_connect(self, conn):
        # Asignar ID y crear archivo en cliente con id
        print(f"[Conexión nueva] {conn}")
        self.Connections.append(conn)
        # code that runs when a connection is created
    
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        return "¡Adios!"

    def exposed_get_files(self): # this is an exposed method
        return self.My_files

    def exposed_write(self, file_name, size, data): # this is an exposed method
        if not self.Minions:
            return "Lo siento. No hay servidores disponibles."

        print(
            "Saving", file_name,
            "size", size,
        )

        # save file in local and append to my_files
        with open(file_name, 'wb') as f:
            f.write(data)
            self.My_files.append(f.name)
        # get blocks
        chunks = self.Get_Chunks(file_name, size)
        
        for minion in self.Minions:
            for i in self.Partitions:
                # Guardar registro de particiones

                # print(i[1])
                c = rpyc.connect("localhost", 18862)
                minion_root = c.root
                minion_root.save_chunks(chunks)



        print("¡Archivo creado exitosamente!")
        return chunks


    def Get_Chunks(self, file, size):
        # get total of blocks
        self.Chunks[file] = []
        blocks = math.ceil(size/CHUNKS_SIZE)
        print("blocks", blocks)
        # Write in minions
        with open(file, 'rb') as f:
            # Recorrer el archivo en bloques de CHUNKS_SIZE bytes
            for i in range(blocks):
                data = f.read(CHUNKS_SIZE)
                id = uuid.uuid4()
                self.Chunks[file].append(id)
                partition = (id, data)
                self.Partitions.append(partition) # data = partitions[i][1]
                                                    # id = partitions[i][0]
        return self.Chunks


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(DfsService(), port=18861, protocol_config={
        'allow_public_attrs': True,
    })
    t.start()
