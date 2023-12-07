# Sistema de Archivos Distribuido en Python con rpyc
En la era digital actual, la gestión eficiente de archivos se ha convertido en una piedra angular para la productividad y la colaboración en entornos profesionales y empresariales. En este contexto, surge la necesidad de un sistema avanzado que no solo permita el almacenamiento y recuperación de archivos, sino que además opere en un entorno distribuido, brindando flexibilidad y escalabilidad. Es en este escenario que nuestro proyecto de software cobra relevancia: un sistema distribuido de manejo de archivos.

## Arquitectura
La arquitectura del sistema se compone de: 
1 Maestro para recibir todas las peticiones de los clientes, 1 Maestro Shadow que estará copiando todos los registros del Maestro original y 4 Servidores Esclavos (Workers) que estarán atendiendo las peticiones del Maestro.
Para resolver el problema de volatibilidad en la memoria de los programas, se generan archivos para los metadatos en el Maestro y llaves de acceso en los Clientes.

### Servidor
Un servidor RPC que corre en el puerto 18861.

### Cliente
Un cliente RPC que se conectará al Master y hará peticiones.

### Worker
Servidores RPC con los directorios en donde se almacenarán los chunks de datos.

### Directorio DFS_v1.2_backups
Este directorio todavía no se usa en el proyecto. Contiene un Script para detectar los archivos entrantes a la carpeta en la que está el Script y crea una copia en el directorio backups. Si el directorio no existe se crea. 

## Al iniciar el servicio
Al correr el servidor Maestro, la memoria del programa se borra y necesita de la conexión de un Worker, esto hace al Servidor leer el archivo cache-metadata/saved-files.json para copiar los objetos con los metadatos de todos los usuarios y archivos al Servidor y poder trabajar. 
El Servidor se crea en una instancia de la clase rpyc.Service. Esta instancia es compartida por todas las conexiones y guarda una lista con los metadatos de todos los archivos y la referencia al Worker en donde reside cada chunk de datos. 

## Autenticación
La autenticación inicia del lado del Cliente o del Worker. Al conectarse al Master la primera petición es a la función Auth_Host(). Esta función decidirá si crear un nuevo usuario o autenticarlo. Esta acción hace que el Cliente o el Worker que se está autenticando genere un nuevo archivo con el nombre “auth.txt” que usará para autenticarse cuando vuelva a ingresar.
Los Clientes no podrán realizar peticiones al Servidor cuando no haya ningún Worker activo.

## Conexión Worker-Master
Al correr un Worker, este se conecta con el Master para autenticarse y registrarse como Worker, si es el primer Worker en conectarse, el Master inicializará su base de datos para empezar a aceptar las peticiones de los Clientes. 

## Guardar archivo
Para guardar un archivo el Cliente proporciona el nombre, el tamaño y los datos del archivo al servidor. Con estos datos el Servidor crea una instancia de la clase File().
El cliente ahora tiene acceso a una función que envía los chunks a los Workers. 
Los chunks que contienen los datos del archivo se reparten de igual forma entre todos los Workers disponibles. 
La instancia del nuevo archivo se escribe en un archivo .json y se guarda en la memoria del programa.
Podríamos decir que separamos el contenido del archivo de toda la referencia a el.

## Descargar archivo
Para leer un archivo el sistema busca en su base de datos, si el archivo existe y el usuario es el dueño, se itera sobre los chunks guardados en el archivo y se conecta con los workers que tengan ese chunk. 
Finalmente los datos se escriben en la caché del cliente. Si el archivo ya existe se le pregunta si desea sobrescribirlo.

## Correr proyecto localmente
Para correr es necesario instalar un ambiente virtual de python en este directorio.

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
