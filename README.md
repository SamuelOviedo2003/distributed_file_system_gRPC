# distributed_file_system_gRPC

## Tópicos Espec. en Telemática - C2466-ST0263-1716

*Presentación y video en el Releases del repositorio*

### Estudiantes: 
- Nicolas Tovar Almanza - ntovara@eafit.edu.co
- Samuel Oviedo Paz - soviedop@eafit.edu.co
- Isis Catitza Amaya Arbeláez - icamayaa@eafit.edu.co
- Santiago Alberto Rozo Silva - sarozos@eafit.edu.co
- Samuel Acosta Aristizábal - sacostaa1@eafit.edu.co
  

### Profesor: 
Alvaro Enrique Ospina Sanjuan  - aeospinas@eafit.edu.co


### Nombre del proyecto:

Tópicos Especiales en Telemática, 2024-2 Proyecto No 1

***Sistemas de archivos distribuidos por bloques***

<hr>

**Presentación:** [Presentacion en CANVA](https://www.canva.com/design/DAGSD1IJskY/jalbEFKO-Uc4F6LgB-v-0Q/edit?utm_content=DAGSD1IJskY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton )

**Video:** [Video en Youtube](https://www.youtube.com/watch?v=d6eNXH6oDZ8)

<hr>

### Documentación
## 1. Breve descripción de la actividad

Diseñar e implementar un sistema de archivos distribuidos por bloques (DFS) minimalista, inspirado en sistemas como GFS y HDFS. El objetivo es crear un sistema que permita almacenar, replicar y acceder a archivos distribuidos en diferentes nodos, garantizando escalabilidad y tolerancia a fallos. Los usuarios interactuarán con el sistema a través de una interfaz de comandos o API, y los archivos se dividirán en bloques que serán distribuidos entre los nodos para su almacenamiento. Se deben implementar mecanismos de replicación de bloques para asegurar la disponibilidad de los datos en caso de fallos.

### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor 

#### Requerimientos Funcionales Cumplidos:
- ***Particionamiento y distribución de archivos en bloques:*** El sistema está orientado a bloques, donde los archivos son distribuidos y gestionados en múltiples nodos (DataNodes).

- ***Interfaz de comandos (CLI):*** La implementación de un cliente con una CLI que permite ejecutar comandos como ls, put, get, entre otros, cumpliendo con el requerimiento funcional de interacción.

- ***Replicación de datos:*** Los bloques están replicados en varios nodos para garantizar la tolerancia a fallos.

- ***Comunicación directa cliente-DataNode:*** El cliente se comunica directamente con los DataNodes para la lectura y escritura de los bloques, cumpliendo con el requerimiento de transferencia directa de datos.

- ***Autenticación básica:*** La autenticación fue implementada para restringir el acceso a los archivos de cada usuario.

#### Requerimientos No Funcionales Cumplidos:
- ***Escalabilidad:*** La implementación en múltiples DataNodes demuestra un diseño escalable, permitiendo agregar más nodos según sea necesario para manejar mayores volúmenes de datos.

- ***Tolerancia a fallos:*** El uso de replicación de bloques entre los DataNodes garantiza que el sistema pueda continuar funcionando incluso si alguno de los nodos falla, cumpliendo con el requerimiento no funcional de alta disponibilidad.

- ***Comunicación eficiente con gRPC:*** gRPC se está utilizando para la comunicación entre el cliente, NameNode y DataNodes, asegurando una baja latencia y un menor consumo de ancho de banda, lo que es fundamental para sistemas de alta concurrencia.

### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor 

Consideramos que se cumplieron con los todos los aspectos propuesto por el profesor.


## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

### Diseño de Alto Nivel: 
El diseño de este sistema sigue una arquitectura distribuida típica para sistemas de archivos. Se ha implementado con la idea de distribuir el almacenamiento de archivos en diferentes nodos, replicar los datos para garantizar la tolerancia a fallos y permitir la escalabilidad horizontal mediante la adición de más nodos.

#### Componentes Clave:
- ***NameNode:*** Es el componente central que gestiona los metadatos del sistema de archivos, incluidos los detalles de particionamiento de bloques, las ubicaciones de los bloques en los DataNodes y la coordinación de la replicación.

- ***DataNodes:*** Son los nodos de almacenamiento donde se guardan los bloques reales de los archivos. Cada DataNode puede recibir bloques desde el cliente, replicarlos en otros DataNodes y responder a solicitudes de lectura y escritura de bloques.

- ***Clientes:*** Los usuarios interactúan con el sistema a través de una CLI. Estos clientes realizan las operaciones de lectura y escritura en el sistema, como put (subir un archivo) y get (descargar un archivo)

### Arquitectura:

La arquitectura sigue el patrón de ***Master-Slave*** (en este caso, NameNode-DataNode):

- ***NameNode:*** Funciona como un "orquestador", manteniendo un mapa lógico del sistema de archivos, supervisando las operaciones y coordinando las transferencias entre los clientes y los DataNodes.

- ***DataNodes:*** Son los "trabajadores" encargados del almacenamiento y replicación de los bloques de datos.
El sistema está diseñado para que los clientes no interactúen directamente con el NameNode para operaciones de lectura y escritura de datos. En su lugar, el NameNode les indica qué DataNodes deben usar, y los clientes realizan las operaciones directamente con estos nodos.

***Comunicación*** 
- ***gRPC:*** El uso de gRPC para la comunicación entre el cliente y los DataNodes asegura una comunicación eficiente de bajo nivel entre servicios distribuidos. Esto reduce la latencia y optimiza el uso del ancho de banda.

- ***Protocolo de Control y Protocolo de Datos:*** El NameNode y los DataNodes se comunican constantemente mediante un "heartbeat" para monitorizar su estado. El canal de control coordina las acciones, mientras que el canal de datos maneja las transferencias de bloques de archivos.

  ![Arquitectura](https://github.com/user-attachments/assets/39769a41-2476-419a-a45b-dc4b6f7aa12a)


### Patrones de Diseño:

- ***Patrón de Orquestación (Orchestrator Pattern):*** El NameNode actúa como un orquestador central que maneja las solicitudes de los clientes y distribuye las tareas a los DataNodes. 

- ***Patrón de Replicación (Replication Pattern):*** Se ha implementado la replicación de bloques, en la que cada bloque es almacenado en varios DataNodes para asegurar la disponibilidad de los datos en caso de fallo de un nodo.

- ***Patrón de Comunicación Asíncrona (Asynchronous Communication Pattern):*** La comunicación entre el cliente y los DataNodes, así como entre el NameNode y los DataNodes, utiliza un enfoque asíncrono para mejorar la eficiencia y la capacidad de respuesta.

### Mejores Prácticas Utilizadas
- ***División en Microservicios:*** El sistema está dividido en varios servicios independientes (NameNode y DataNodes), cada uno con su propia responsabilidad bien definida, lo que sigue el principio de separación de preocupaciones. Esto facilita el mantenimiento y la escalabilidad del sistema.

- ***Uso de gRPC:*** Se ha utilizado gRPC para la comunicación entre componentes, lo que es una buena práctica para sistemas distribuidos que requieren baja latencia y eficiencia de red. gRPC permite una serialización eficiente y una comunicación más rápida que REST en entornos distribuidos.

- ***Replicación de Datos para Tolerancia a Fallos:*** La replicación de bloques en múltiples DataNodes es una práctica estándar en sistemas distribuidos para asegurar la tolerancia a fallos. Al replicar bloques, se asegura que el sistema pueda seguir funcionando incluso si uno de los nodos falla.

- ***Tolerancia a Fallos:***  Al replicar bloques entre DataNodes, se garantiza la disponibilidad de los datos incluso si uno de los nodos falla, cumpliendo con el principio de alta disponibilidad.
## 3. Descripción del ambiente de desarrollo y técnico: 

### Lenguaje de programación

El proyecto está desarrollado en **Python**

### Librerias y paquetes:
- ***gRPC:*** Utilizado para la comunicación entre el Cliente, NameNode, y DataNodes.
  
  - **Paquete:** grpcio
    
  - **Paquete para generar archivos protobuf:** grpcio-tools
    
- ***protobuf:*** Utilizado para definir la estructura de los datos que se envían entre los nodos. 

  - **Paquete:** protobuf
    
- ***Docker:*** Utilizado para contenerizar los diferentes componentes (NameNode, DataNode, Cliente) y facilitar el despliegue en la nube.

  - **Archivo de configuración:** Dockerfile (posiblemente en cada componente).

- ***pytest:*** Utilizado para ejecutar pruebas unitarias del sistema. Facilita la validación de las funciones del sistema para asegurar su correcto funcionamiento.
  - **Paquete:** pytest

- ***os:*** Biblioteca estándar de Python para operaciones del sistema operativo, como la gestión de archivos y directorios.

- ***sys:*** Utilizado para manejar parámetros del sistema y configuración de ejecución.

- ***logging:*** Utilizado para la gestión de logs del sistema, lo que permite hacer un seguimiento detallado de las operaciones en los DataNodes, NameNode, y Cliente.

### Detalles del desarrollo.
***Comunicación entre componentes:***  Los archivos de definición de protobuf (.proto) especifican los servicios y mensajes que se utilizan para las transferencias de datos.

***Particionamiento de archivos:***  Los archivos son divididos en bloques en el Cliente y distribuidos en los DataNodes. Se implementa un algoritmo para la asignación de bloques, asegurando que los archivos sean replicados en al menos dos DataNodes.

***Replicación de datos:*** Se utiliza replicación entre DataNodes para asegurar tolerancia a fallos, implementando un esquema en el que uno de los DataNodes actúa como Leader y el otro como Follower.

***Monitoreo y Heartbeat:*** El NameNode monitorea el estado de los DataNodes mediante un mecanismo de "heartbeat", verificando continuamente la disponibilidad de los nodos

**Estructura del Código:**
El proyecto tiene una estructura modular que facilita el desarrollo y mantenimiento

<div align="center">
  
![image](https://github.com/user-attachments/assets/1be9b48d-8f60-4d2d-9a86-f1cb1a08c2a3)

</div>


## 4. Referencias:
- https://techvidvan.com/tutorials/how-hadoop-works-internally/
- https://www.simplilearn.com/tutorials/hadoop-tutorial/what-is-hadoop
- https://www.youtube.com/watch?v=CTdc67MMaL8&t=3s
- https://www.youtube.com/watch?v=eRgFNW4QFDc&t=4s
- https://www.youtube.com/watch?v=u4o-th2T9KA&t=3s
- https://pages.cs.wisc.edu/~akella/CS838/F15/838-CloudPapers/hdfs.pdf
- https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf 
