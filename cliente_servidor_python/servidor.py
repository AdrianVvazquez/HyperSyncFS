import socket
import json
import os

# Enlace de socket y puerto
# SERVER_ADDRESS = ('192.168.0.16', 22)
SERVER_ADDRESS = ('148.239.119.53', 22)

def connection():
    # Creando el socket TCP/IP
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Empezando a levantar %s puerto %s' % SERVER_ADDRESS)
    serversocket.bind(SERVER_ADDRESS)   # Asociar socket a direccion
    # Escuchando conexiones entrantes
    serversocket.listen(1)
    return serversocket

msn_1 = 'Hola cliente, te conectaste a servidor, bienvenido.'
serversocket = connection()
amount_expected = 60
amount_received = 0


while True:
    # Esperando conexion
    print('Conectando...')
    (connection, client_address) = serversocket.accept()

    try:
        print('Conexión desde', client_address, "\n")
        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(amount_expected)
            if data:
                amount_received += len(data)
                print('Recibido: "%s"' % data.decode("utf-8"))
                print('Enviando... mensaje al cliente...')
                connection.sendall(msn_1.encode("utf-8"))
                recv = json.loads(data)
                print(recv)
                # file_name = data['file_name']
                # f = open(f"{file_name}.txt", "x")
                # f.write(data.content + "\n")
                # Cierra el archivo
                # f.close()
            else:
                print('\nNo hay mas datos. Finalizando transmisión con...', client_address)
                break
        
            
    finally:
        # Cerrando conexion
        connection.close()

# try:
#     print('Conexión desde', client_address, "\n")
#     # Recibe los datos en trozos y reetransmite
#     while True:
#         data = connection.recv(len(msn_1))
#         if data:
#             print('Recibido: "%s"' % data.decode("utf-8"))
#             print('Enviando... mensaje al cliente...')
#             connection.sendall(msn_1.encode("utf-8"))
#             # Convierte el dato en JSON
#             data_json = json.dumps(data)
#             # Abre el archivo en modo append
#             f = open("data.txt", "a")
#             # Escribe el JSON en el archivo
#             f.write(data_json + "\n")
#             # Cierra el archivo
#             f.close()
#             # Convierte el JSON en un diccionario
#             data_dict = json.loads(data_json)
#             # Obtiene el campo nombre del diccionario
#             nombre = data_dict["nombre"]
#             # Imprime el nombre
#             print("El nombre es:", nombre)
#         else:
#             print('\nNo hay mas datos. Finalizando transmisión con...', client_address)
#             break
