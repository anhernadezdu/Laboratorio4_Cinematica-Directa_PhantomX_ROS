# Laboratorio4_Cinematica-Directa_PhantomX_ROS
## Mediciones y Analisis
Se utilizo un pie de rey con resolucion de 0.05mm para hallar las longitudes de los eslabones de lrobot Phantom X. A continuacion se muestra el diagrama de las medidas del robot.

Seguidamente se procedio a hallar los parametros DH usando las dimensiones medidas y el siguiente diagrama; obteniendo asi los paramteros en la tabla:
|Articulacion| Theta    | D    | Alpha | A    |
| :---:      | :---:    |:---: |:---:  |:--:  |
| 1          |Q1        | L1   |pi/2   |0     |
| 2          |Q2+pi/2   | 0    |0      |L2    |
| 3          |Q3        | 0    |0      |L3    |
| 4          |Q4        | 0    |0      |L4    |
## Toolbox
Hechos con los parametros DH se realizo el siguiente codigo en matlab [CinDirMatlab]() donde usando la Toolbox el Modelo Cinematico Directo, se crearon las imagenes virtuales de las posiciones que el robot PhantomX real a de tener, con el codigo presentado mas adelante donde se realiza la conexion con Python y ROS.
## Solucion Planteada
Primeramente se procedio a crear un nuevo workspace con el comando `catkin_make`, y dentro de la carpeta src del mismo se procedio a clonar el repositorio de [dynamixel_one_motor](https://github.com/fegonzalez7/dynamixel_one_motor.git) proporcionado en la guia del laboratorio. Dado que este repositorio esta hecho para el manejo de un solo servomotor, apoyados en el analisis del paquete [px_robot](https://github.com/felipeg17/px_robot.git) para controlar los 5 motores del robot PhantomX, se procedio a:

1. Modificar el archivo **CMakeLists** del paquete one_controller de tal forma que copie el formato del archivo con el mismo nombre, enocntrado en el paquete *px_robot*, y asi peuda identificar y asignar un controlador dynamixel; del paquete previamente instalado *dynamixel_workbench_controller*, a cada servomotor o articualcion del robot.
2. C
### Video Funcionamiento

### Comparacion Robot Real con Obtenida por Toolbox
