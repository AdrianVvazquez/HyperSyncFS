import socket
import json
# SERVER_ADDRESS = ('192.168.0.16', 22)
SERVER_ADDRESS = ('148.239.112.235', 22)

def menu(opc=0):
    if opc == 0:
        opc = int(input("Bienvenido.\n\n [1] Subir archivo de texto.\n [2] Ver archivos disponibles.\n"))
        menu(opc)
    
    elif opc == 1:
        file_name = input("Nombre: ")
        content = input(f"\n\t{file_name}.txt\n")
        message = {
            "file_name": file_name,
            "content": content,
        }
        print("#print1", message['file_name'])
        return message
    
    else: 
        print("Opción inválida.\n")
        menu(0)

def connection():
    # Creando un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # An INET, STREAMing socket
    # print('Conectando a %s puerto %s ...\n' % SERVER_ADDRESS)
    sock.connect(SERVER_ADDRESS)
    return sock

while(True):
    # Conecta el socket en el puerto cuando el servidor esté escuchando.
    sock = connection()
    # Correr la interfaz y hacer la conexión.
    message = menu(0)
    # message2 = "Hola servidor. Soy cliente."
    amount_expected = 2 # ok
    amount_received = 0

    print("Msg len:", len(json.dumps(message).encode('utf-8')))
    try:
        # Enviando datos
        print('Enviando... "%s"' % json.dumps(message).encode('utf-8'))
        sock.sendall(json.dumps(message).encode('utf-8'))

        # Buscando respuesta
        while True:
            data = sock.recv(amount_expected)
            amount_received += len(data)
            print('Recibido: "%s"' % data.decode("utf-8"))

    except:
        print("\nOcurrió un error.\n")

    finally:
        print("\nCerrando socket... \nFinalizó conexión.")
        sock.close()


# https://pythondiario.com/2015/01/simple-programa-clienteservidor-socket.html
