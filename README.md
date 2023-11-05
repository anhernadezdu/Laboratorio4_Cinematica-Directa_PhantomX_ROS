# Laboratorio4_Cinematica-Directa_PhantomX_ROS
## Mediciones y Analisis
Se utilizo un pie de rey con resolucion de 0.05mm para hallar las longitudes de los eslabones de lrobot Phantom X. A continuacion se muestra el diagrama de las medidas del robot.
![WhatsApp Image 2023-11-05 at 16 40 48](https://github.com/anhernadezdu/Laboratorio4_Cinematica-Directa_PhantomX_ROS/assets/70985250/a377600d-ea08-4925-9c87-8452264b8a1c)
Seguidamente se procedio a hallar los parametros DH usando las dimensiones medidas y el siguiente diagrama.
![WhatsApp Image 2023-11-05 at 17 34 04](https://github.com/anhernadezdu/Laboratorio4_Cinematica-Directa_PhantomX_ROS/assets/70985250/dec1d7c5-23cb-49cc-af59-45a39b6eee17)
Obteniendo asi los paramteros en la tabla:
|Articulacion| Theta    | D    | Alpha | A    |
| :---:      | :---:    |:---: |:---:  |:--:  |
| 1          |Q1        | L1   |pi/2   |0     |
| 2          |Q2+pi/2   | 0    |0      |L2    |
| 3          |Q3        | 0    |0      |L3    |
| 4          |Q4        | 0    |0      |L4    |
## Toolbox
Hechos con los parametros DH se realizo el siguiente codigo en matlab [CinDirMatlab](CinDirPhantom.m) donde usando la Toolbox el Modelo Cinematico Directo, se crearon las imagenes virtuales de las posiciones que el robot PhantomX real a de tener, con el codigo presentado mas adelante donde se realiza la conexion con Python y ROS.
## Solucion Planteada
Primeramente se procedio a crear un nuevo workspace con el comando `catkin_make`, y dentro de la carpeta src del mismo se procedio a clonar el repositorio de [dynamixel_one_motor](https://github.com/fegonzalez7/dynamixel_one_motor.git) proporcionado en la guia del laboratorio. Dado que este repositorio esta hecho para el manejo de un solo servomotor, apoyados en el analisis del paquete [px_robot](https://github.com/felipeg17/px_robot.git) para controlar los 5 motores del robot PhantomX, se procedio a:

1. Modificar el archivo **basic.yaml** del paquete one_controller de tal forma que copie el formato del archivo con el misma extension encontrado en el paquete *px_robot* como **joints.yaml**, y asi pueda identificar y asignar un controlador dynamixel; del paquete previamente instalado *dynamixel_workbench_controllers*, a cada servomotor o articulacion del robot. Este archivo modificado es el [jointsPhantom](jointsPhantom.yaml) .
2. Seguidamente se cambio el archivo launch del paquete one_controller por el archivo [phantom.launch](phantom.launch) donde se especifica que para la identificacion de motores y asignacion de controladores; se va a hacer bajo los parametros del archivo *jointsPhantom* donde se asigna Nombre, ID, torque Maximo y velocidad de movimeinto, especificos a cada motor.
3. Seguidamente usando los scipts de python de one_controller, se crea el script [Interfaz.py](Interfaz.py). En este srcipt, aparte de tener la creacion de la interfaz de usuario que se mostrara mas adelante, contiene una funcion para llamar al servicio de *dynamixel_command* para ejecutar los movimientos de los motores al ingresar *'Goal_Position'* al parametro addr_name.
```
def jointCommand(command, id_num, addr_name, value, time):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        ...
```
Tambien contiene funciones para la creacion de un publisher y un listener, los cuales realizan distintas acciones. El primero se comunica con el nodo maestro mediante otro nodo para enviar informacion de estado de articulaciones o *joint_states* y el segundo crea otro nodo para poder suscribirse al *topic* mencionado previamente y asi poder procesar la informacion de la nueva posicion de cada motor y poder ejecutar o hacer us odel siguiente servicio a utilizar.
```
def listener():
    rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)
    
def joint_publisher():
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)
    ...
```
Tambien cuenta con una funcion *callback* la cual guarda el dato del objeto de tipo JointState, el cual contiene las posiciones, velocidades, aceleraciones y torques de cada motor al momento de llamarse la funcion.
4. Finalmente, por fines esteticos, se realiza una modificacion en el archivo [CMakeLists](CMakeLists.txt) para asi permitir el incluir la carpeta [resources](resources), que contiene el logo de la Unal, junto con los el script Interfaz.py dentro del paquete one_controller.

### Video Funcionamiento con Interfaz grafica



### Comparacion Robot Real con Obtenida por Toolbox


