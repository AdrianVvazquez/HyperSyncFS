# Systema de Archivos Distribuido en Python con rpyc

Para correr es necesario instalar un ambiente virtual de python en este directorio.

## Descripción
### Directorio DFS_v1.2_backups
Contiene un Script para detectar los archivos entrantes a la carpeta en la que está el Script y crea una copia en el directorio backups. Si el directorio no existe se crea.


### Directorio DFS_v2_connection
## Servidor
Un servidor RPC que corre en el puerto 18861.
Guardar metadatos.

## Cliente

## Worker
Los servidores con los directorios en donde se almacenarán los chunks de datos.

```bash
py -m venv venv
```
Después de activar el ambiente virtual instala las librerías del archivo de requerimientos:
```bash
pip install -r requirements.txt
```


## Tutoriales de referencia e inspiración
- https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
- https://github.com/sanketplus/PyDFS/blob/srecon/pydfs/master.py
