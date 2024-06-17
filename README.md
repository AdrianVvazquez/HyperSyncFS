# 🗃️ Sistema de Archivos Distribuido en 🐍Python con rpyc 
📄 La gestión eficiente de archivos se ha convertido en una piedra angular para la productividad y la colaboración en entornos profesionales y empresariales. 

En este contexto, introducimos nuestro propio sistema distribuido de archivos. ¡Con almacenamiento y recuperación de archivos avanzado! ¡Opera en un entorno distribuido, brindando flexibilidad y escalabilidad!

## Características funcionales:
- Metadatos: Master genera estos archivos y los guarda en formato JSON o texto plano. El Servidor Master guarda una lista con objetos de metadatos de todos los archivos y las referencias al Worker en donde reside cada chunk de datos que forma un archivo. 
- Acceso: Master genera llaves de acceso para los Clientes y los registra como usuarios conocidos. La autenticación empieza con una petición del Cliente a Master.
- Copias de seguridad: Contiene un script para detectar los archivos añadidos a tu carpeta local. Los Workers crean una copia de todos los archivos en el directorio local "/backups". Si el directorio "backups" no existe se crea uno nuevo.
- Frontend: Se usa la misma interfaz de usuario del sistema de archivos local de Windows, Mac y Linux.

## 🔑 Autenticación 
La autenticación inicia del lado del Cliente o del Worker. La primera petición de conexión que recibe Master va directo a la función Auth_Host(). Esta función decidirá si autorizar al usuario o iniciar con el proceso de autentización. El proceso de autenticación de la primera conexión genera un nuevo archivo con el nombre “auth.txt” en el Cliente, que usará para autenticarse cuando vuelva a ingresar.
Los Clientes no podrán realizar peticiones al Servidor cuando no haya ningún Worker activo.

## 🔗 Conexión Worker-Master 
Al correr un Worker, este se conecta con el Master para autenticarse y registrarse como Worker, si es el primer Worker en conectarse, el Master inicializará su base de datos para empezar a aceptar las peticiones de los Clientes. 

## ⬇️ Guardar un archivo 
- Para guardar un archivo el Cliente proporciona el nombre, el tamaño y los datos del archivo al servidor. 
- Con estos datos el Servidor Master crea una instancia de la clase File() para los metadatos.
- El cliente ahora tiene acceso a una función con la que reparte los chunks a los Workers. 
- Los chunks llevan el contenido del archivo y se reparten de igual forma entre todos los Workers disponibles.
- La instancia con los metadatos del nuevo archivo se escribe en un archivo .json y se guarda en la memoria del programa.
Podríamos decir que separamos el contenido del archivo de toda la referencia a el.

## ⬆️ Descargar un archivo 
Para leer un archivo el sistema busca en su base de datos, si el archivo existe y el usuario es el dueño, se itera sobre los chunks guardados en el archivo y se conecta con los workers que tengan ese chunk. 
Finalmente los datos se escriben en la caché del cliente. Si el archivo ya existe se le pregunta si desea sobrescribirlo.

## Arquitectura del sistema
Se aplicó una arquitectura de componentes en donde el registro de usuarios y la gestión de archivos se basa en 3 nodos.
### Servidor
Un servidor RPC corriendo en el puerto 18861.
### Cliente
Un cliente RPC con conexión al host Master.
### Worker
Servidores RPC con permisos de almacenamiento.

Estos nodos son replicados, cada uno con diferentes funciones:
- 1 - Servidor Master para balanceo de cargas, registrar eventos y autenticación de usuarios.
- 1 - Servidor Master Shadow para suplir al Master original en caso de desconexión. Copia casi todos los pasos del Master original, se mantiene "inactivo" y puede suplir perfectamente al Master.
- 4 - Servidores Esclavos (Workers) que estarán atendiendo peticiones del Maestro y ejecutando consultas a la base de datos.

## Correr proyecto localmente
Para correr es necesario instalar un ambiente virtual de python en este directorio.

```bash
py -m venv venv
```
Después de activar el ambiente virtual instala las librerías del archivo de requerimientos:
```bash
pip install -r requirements.txt
```

## 👀 Al reiniciar un Master
Cuando un Cliente guarda un archivo primero Master genera un objeto para los metadatos del archivo en la memoria del programa, la cual se borra al reiniciar el servicio. Cuando el Servidor iniciar y detecta que no tiene memoria para trabajar busca un archivo llamado "cache-metadata/saved-files.json" para copiar los objetos de los metadatos de todos los usuarios y archivos a la memoria y empezar a trabajar. 

## Tutoriales de referencia e inspiración
- https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
- https://github.com/sanketplus/PyDFS/blob/srecon/pydfs/master.py
