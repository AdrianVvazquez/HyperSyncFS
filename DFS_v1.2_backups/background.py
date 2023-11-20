import os
import shutil
import time

def crear_copia(archivo, directorio_destino):
    nombre_archivo = os.path.basename(archivo)
    copia_destino = os.path.join(directorio_destino, nombre_archivo)
    shutil.copy2(archivo, copia_destino)
    print(f"Creada copia de {nombre_archivo} en {directorio_destino}")

def monitorear_directorio(directorio, directorio_destino, exclusiones):
    archivos_previos = set()

    while True:
        archivos_actuales = set(os.listdir(directorio))

        # Comprueba si hay nuevos archivos
        archivos_nuevos = archivos_actuales - archivos_previos

        for archivo in archivos_nuevos:
            ruta_archivo = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_archivo) and not any(excluye in archivo for excluye in exclusiones):
                crear_copia(ruta_archivo, directorio_destino)

        archivos_previos = archivos_actuales

        # Espera antes de volver a verificar
        time.sleep(1)

if __name__ == "__main__":
    directorio_actual = os.getcwd()
    directorio_backups = os.path.join(directorio_actual, "backups")

    # Crea el directorio de backups si no existe
    if not os.path.exists(directorio_backups):
        os.makedirs(directorio_backups)

    # Lista de archivos a excluir de los backups
    archivos_a_excluir = [".gitattributes", "background.py"]

    print(f"Monitoreando el directorio {directorio_actual}...")

    monitorear_directorio(directorio_actual, directorio_backups, archivos_a_excluir)
