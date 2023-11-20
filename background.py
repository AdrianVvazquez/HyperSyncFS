# Importar el módulo os para trabajar con archivos y directorios
import os

# Definir el directorio actual como el directorio de trabajo
dir_actual = os.getcwd()

# Crear una función que copie un archivo dado a otro con el mismo nombre y la extensión .bak
def copiar_archivo(archivo):
    # Abrir el archivo original en modo lectura binaria
    with open(archivo, "rb") as original:
        # Leer el contenido del archivo original
        contenido = original.read()
        # Crear el nombre del archivo de copia añadiendo .bak al final
        copia = archivo + ".bak"
        # Abrir el archivo de copia en modo escritura binaria
        with open(copia, "wb") as backup:
            # Escribir el contenido del archivo original en el archivo de copia
            backup.write(contenido)
            # Cerrar el archivo de copia
            backup.close()
    # Cerrar el archivo original
    original.close()

# Crear una lista vacía para almacenar los nombres de los archivos que ya existen en el directorio actual
archivos_existentes = []

# Recorrer los archivos que hay en el directorio actual
for archivo in os.listdir(dir_actual):
    # Añadir el nombre del archivo a la lista de archivos existentes
    archivos_existentes.append(archivo)

# Crear un bucle infinito
while True:
    # Recorrer los archivos que hay en el directorio actual
    for archivo in os.listdir(dir_actual):
        # Comprobar si el archivo no está en la lista de archivos existentes
        if archivo not in archivos_existentes:
            # Llamar a la función copiar_archivo con el nombre del archivo como argumento
            copiar_archivo(archivo)
            # Añadir el nombre del archivo a la lista de archivos existentes
            archivos_existentes.append(archivo)
