# 🗃️ Sistema de Archivos Distribuido en 🐍Python con rpyc

La gestión eficiente de archivos es una piedra angular para la productividad y la colaboración en entornos profesionales y empresariales.
En este contexto, presentamos un sistema distribuido de archivos con almacenamiento y recuperación avanzados, operando en un entorno distribuido que brinda flexibilidad y escalabilidad.

---

## ✨ Características Funcionales

### 📁 Metadatos

* El Servidor Master genera archivos en formato JSON o texto plano.
* Guarda una lista de objetos de metadatos y referencias a los Workers donde reside cada *chunk* de datos.

### 🔐 Acceso

* El Master genera llaves de acceso para los Clientes y los registra como usuarios conocidos.
* La autenticación comienza con una petición del Cliente al Master.

### 💾 Copias de Seguridad

* Un script detecta archivos nuevos en la carpeta local.
* Los Workers crean una copia de todos los archivos en el directorio `/backups`.
* Si no existe el directorio `/backups`, se crea automáticamente.

### 🖥️ Frontend

* Se utiliza la interfaz de usuario nativa del sistema operativo (Windows, Mac, Linux).

---

## 🔑 Autenticación

1. Inicia del lado del Cliente o Worker.
2. La primera conexión al Master invoca la función `Auth_Host()`.
3. Esta función decide si autorizar o iniciar la autenticación.
4. Se genera un archivo `auth.txt` en el Cliente para futuras autenticaciones.
5. No se permiten peticiones al Servidor si no hay Workers activos.

---

## 🔗 Conexión Worker-Master

* Un Worker se conecta al Master para autenticarse y registrarse.
* Si es el primer Worker, el Master inicializa su base de datos para aceptar peticiones.

---

## ⬆️ Guardar un Archivo

1. El Cliente envía nombre, tamaño y datos del archivo al Servidor.
2. El Master crea una instancia de la clase `File()` con los metadatos.
3. El Cliente accede a una función que reparte los *chunks* entre los Workers.
4. Los *chunks* contienen el contenido del archivo y se distribuyen equitativamente.
5. Los metadatos se guardan como un archivo `.json` en memoria.

---

## ⬇️ Descargar un Archivo

1. Se busca el archivo en la base de datos.
2. Si existe y el usuario es el dueño:

   * Se localizan los *chunks* y los Workers correspondientes.
   * Los datos se descargan y almacenan en caché.
   * Si el archivo ya existe, se solicita confirmación para sobrescribirlo.

---

## 🏗️ Arquitectura del Sistema

Se implementa una arquitectura de componentes con 3 tipos de nodos:

### 🖥️ Servidor

* RPC activo en el puerto `18861`.

### 👤 Cliente

* RPC con conexión al Master.

### ⚙️ Worker

* Servidores RPC con permisos de almacenamiento.

#### Distribución de Nodos

* `1` Master: balanceo de carga, eventos y autenticación.
* `1` Shadow Master: suplente en caso de falla del Master, copia su comportamiento y entra en acción automáticamente.
* `4` Workers: ejecutan peticiones y consultas de almacenamiento.

---

## 🧪 Ejecutar Proyecto Localmente

1. Crea un entorno virtual:

   ```bash
   py -m venv venv
   ```

2. Activa el entorno virtual y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔄 Reinicio del Master

1. Al guardar un archivo, se crea un objeto de metadatos en memoria (se pierde al reiniciar).
2. Al iniciar, el Master busca el archivo `cache-metadata/saved-files.json` para restaurar los metadatos.

---

## 📚 Tutoriales de Referencia e Inspiración

* [RPyC Tutorial](https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html)
* [PyDFS en GitHub](https://github.com/sanketplus/PyDFS/blob/srecon/pydfs/master.py)
