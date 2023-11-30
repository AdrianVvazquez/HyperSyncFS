import os
import sys
import rpyc

def authenticate(master, user_name, ip, port):
    print(f"\nBIENVENIDO {user_name}")
    try:
        with open('auth.txt', 'r+') as f:
            # Autenticar por user_name
            credentials = [line.strip().split('/') for line in f if user_name in line]
            if credentials:
                _host_name, key = credentials[0]
                print("#"*50)
                print('Mi id: ', key)
                print("#"*50, '\n')
            else:
                print("[Error]: No existe ningún usuario con tu username.")
                
    
    except FileNotFoundError:
        # Crear archivo de autenticación
        with open("auth.txt", "w") as f:
            host_id = master.Add_Host(user_name, ip, port)
            f.write(user_name+'/'+host_id)
            print("#"*50)
            print(f'Tu usuario para server auth: {user_name}')
            print(f'ID generado en auth.txt: {host_id} para server auth')
            print("#"*50, '\n')

    except ValueError:
        print("[Error]: Autenticación. Borra el archivo auth.txt y vuelve a correr el programa.")


def get_file(master, host_id, sourceDir):
    # from pathlib import Path
    chunks = master.read(host_id, sourceDir)

    # remote exception
    metadata = chunks[:2]
    if metadata[0] == 'err':
        sys.stdout.write(metadata[1])
        exit(1)
    
    # save in cache
    with open(f'cache/{sourceDir.split(".")[0]}-cache.txt', 'wb+') as f:
        for chunk in chunks:
            f.write(chunk[3])
    
    # local exception
    if os.path.exists(sourceDir):
        opc = ''
        while opc != 'Y' and opc != 'y':
            opc = input("El archivo ya existe en tu máquina... ¿Sobrescribir archivo? Y/n: ")
            if opc == 'N' or opc == 'n':
                exit(1)
        
        # Escribir local
        print("Guardando '"+sourceDir+"'...")
        with open(sourceDir, 'wb+') as f:
            for chunk in chunks:
                f.write(chunk[3])
        print("¡Archivo guardado exitosamente!\n")


def put_file(master, sourceFile, host_id):
    try:
        size = os.path.getsize(sourceFile) # get file size
        with open(sourceFile, "rb") as f:  # send data in binary
            response = master.write(f.name, size, f.read(), host_id)  # write
            
            # exception
            metadata = response[:2]
            if metadata[0] == 'err':
                sys.stdout.write(metadata[1])
                exit(1)
            
            print("¡Archivo creado exitosamente!")
            print("file id: ", response)
            
    except FileNotFoundError:
        print("El archivo especificado no existe.")



def main(args):
    os.path.join
    # TODO: userName = input("User name: ")
    user_name = 'adrian'
    ip = 'localhost'
    port = 18861

    conn = rpyc.connect("localhost", 18861)
    master = conn.root
    # authenticate user
    host_id = authenticate(master, user_name, ip, port)

    if args[0] == "get":
        get_file(master, host_id, args[1]) # get source.txt 
    elif args[0] == "put":
        put_file(master, args[1], host_id) # put source.txt
    else:
        print("try 'put srcFile destFile OR get file'")

    conn.close()

if __name__ == "__main__":
    main(sys.argv[1:])

