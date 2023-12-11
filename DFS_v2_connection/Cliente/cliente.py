import os
import sys
import rpyc

CHUNKS_NUMBER = 0
CHUNKS_SIZE = 1
PERMISSION_READ = 'r'
PERMISSION_WRITE = 'w'
PERMISSION_APPEND = 'a'
PERMISSION_READBINARY = 'rb'
PERMISSION_WRITEBINARY = 'wb'
ERRORLABEL = 0
ERRORINFO = 1

def authenticate(master, user_name, ip, port):
    print(f"\nBIENVENIDO {user_name}")
    try:
        with open('auth.txt', 'r') as f:
            # Autenticar por user_name y key
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
        # Usuario nuevo: Crear archivo de autenticación y registrarse
        print("#"*50)
        print("¡Gracias por usar SUPER_DFS por primera vez!\nEste es un usuario de regalo para que empieces a crear y compartir tus archivos.")
        with open("auth.txt", "w") as f:
            key = master.Auth_Host(user_name, ip, port)
            f.write(user_name+'/'+key)
            print("-"*50)
            print(f'Tu usuario para server auth: {user_name}')
            print(f'ID generado en auth.txt: {key} para server auth')
            print("#"*50, '\n')
            return key

    except ValueError:
        print("[Auth Error]: Borra el archivo auth.txt y vuelve a correr el programa.")

def get_cache_file(fileName):
    return f'cache/{fileName.split(".")[0]}-cache.txt'

def write_cache(fileName, data_chunks):
    cache_file = get_cache_file(fileName)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    # Abrimos el archivo cache en modo escritura
    with open(cache_file, 'wb') as f:
        # Iteramos sobre los chunks del archivo original
        for data in data_chunks:
            # Escribimos el chunk en el archivo cache
            f.write(data)

def get_file(master, userName, sourceFile):
    # save in cache
    cache_file = get_cache_file(sourceFile)
    resp = master.read(userName, sourceFile, write_cache)
    # remote exception
    if resp and resp[:2][ERRORLABEL] == 'err':
        print(resp[:2][ERRORINFO])
        exit(1)
    
    # local exception
    if os.path.exists(sourceFile):
        opc = ''
        while opc != 'Y' and opc != 'y':
            opc = input("El archivo ya existe en tu máquina... ¿Sobrescribir archivo? Y/n: ")
            if opc == 'N' or opc == 'n':
                print(f"No se guardó '{sourceFile}'\n")
                exit(1)
        
        # Sobrescribir
        print(f"Guardando '{sourceFile}'...")
        with open(sourceFile, 'wb') as f1:
            with open(cache_file, 'rb') as f2:
                # Leemos el contenido del archivo 2 como una lista de líneas
                lines = f2.readlines()
                # Escribimos cada línea en el archivo 1
                for line in lines:
                    f1.write(line)
        print("¡Archivo guardado exitosamente!\n")
    else:
        # Guardar
        print(f"Guardando '{sourceFile}'...")
        with open(sourceFile, 'wb') as f1:
            with open(cache_file, 'rb') as f2:
                # Leemos el contenido del archivo 2 como una lista de líneas
                lines = f2.readlines()
                # Escribimos cada línea en el archivo 1
                for line in lines:
                    f1.write(line)
        print("¡Archivo guardado exitosamente!\n")



def put_file(master, sourceFile, userName):
    try:
        file_size = os.path.getsize(sourceFile) # get file size
        # send file header
        send_chunk_func, blocks_info = master.write(sourceFile, file_size, userName)
        if send_chunk_func == 'err':
            print(blocks_info)
            exit(1)

        # write data
        with open(sourceFile, "rb") as f:  # send data in binary
            for n in range(blocks_info[CHUNKS_NUMBER]):
                resp = send_chunk_func(sourceFile, f.read(blocks_info[CHUNKS_SIZE]))
                # exception
                if resp and resp[:2][ERRORLABEL] == 'err':
                    sys.stdout.write(resp[:2][ERRORINFO])
                    exit(1)
            # good
        print("¡Archivo creado exitosamente!")
            
    except FileNotFoundError:
        print("El archivo especificado no existe.")


def write__(cache_file, chunks):
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, 'wb') as f:
        for chunk in chunks:
            print(chunk)
            # f.write(chunk[3])

def main(args):
    os.path.join
    # TODO: userName = input("User name: ")
    user_name = input("User name: ")
    # user_name = 'adrian'
    ip = 'localhost'
    port = 18861

    conn = rpyc.connect("localhost", 18861)
    master = conn.root
    # authenticate user
    auth_key = authenticate(master, user_name, ip, port)

    if args[0] == "get":
        get_file(master, user_name, args[1]) # get source.txt 
    elif args[0] == "put":
        put_file(master, args[1], user_name) # put source.txt
    else:
        print("try 'put srcFile destFile OR get file'")

    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])

