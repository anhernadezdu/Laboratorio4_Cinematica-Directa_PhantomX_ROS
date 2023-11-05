import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import rospy
import rospkg
import os
import numpy as np
from cmath import pi
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from dynamixel_workbench_msgs.srv import DynamixelCommand

#se debe crear nodo para poder publicar el topic de posicion de motores o joint trajectory,
#  y comunicarse con el master node
def joint_publisher():
    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size=0)
    rospy.init_node('joint_publisher', anonymous=False)
    while not rospy.is_shutdown():
        state = JointTrajectory()
        state.header.stamp = rospy.Time.now()
        state.joint_names = ["joint_1"]
        point = JointTrajectoryPoint()
        point.positions = [0, 0, 0, 0, 0]    
        point.time_from_start = rospy.Duration(0.5)
        state.points.append(point)
        pub.publish(state)
        print('published command')
        rospy.sleep(1)

# callback se hace para recodar datos pasados o actuales de posicion
# sirve para establecer diferencia entre pos. pasada y actual osea limite articular
# se crea nodo para suscripcion a topic de estado de articualciones
def callback(data):
    global PosNueva
    PosNueva=np.multiply(data.position, 180/pi)
    #PosNueva=data.position
    #se usa multiply para multiplicar la matriz de posiciones pasadas y convertirlas a grados

def listener():
    rospy.init_node('joint_listener', anonymous=True)
    rospy.Subscriber("/dynamixel_workbench/joint_states", JointState, callback)

#para ejecutar movimientos con Goal_Position o ajustar torque con Torque_Limit 
#usando servicios dynamixel_command
def jointCommand(command, id_num, addr_name, value, time):
    rospy.wait_for_service('dynamixel_workbench/dynamixel_command')
    try:        
        dynamixel_command = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
        result = dynamixel_command(command,id_num,addr_name,value)
        rospy.sleep(time)
        return result.comm_result
    except rospy.ServiceException as exc:
        print(str(exc))

def generate_text(text):
    text_box.insert(tk.END, text)

def posicion(pos):
    if pos==1:
        return "Home"
    elif pos==2:
        return "Pos1"
    elif pos==3:
        return "Pos2"
    elif pos==4:
        return "Pos3"
    elif pos==5:
        return "Pos4"



# Function for the buttons
def button_click(pos):
    global ultPos
    posiElegida=ListaPosiciones[pos-1]
    posiElegidaDegree=ListaPosicionesDegree[pos-1]
    text_box.delete(1.0, tk.END) 
    for i in range(5):
        jointCommand('', i+1, 'Goal_Position', posiElegida[i] ,0.75)
    line="Valores actuales de las Articulación  en grados: "+ "\n"+ "Ultima Posicion enviada: "+str(posicion(ultPos))+ "\n"
    ultPos=pos
    for i  in range(5):
        line=line+"Art."+ Nombres[i]+" = "+str("{0:.2f}".format(PosNueva[i]))+ " Error :"+str("{0:.2f}".format(abs(PosNueva[i]-posiElegidaDegree[i])))+ "\n"
    generate_text(line)


def crearInterfaz():
    root = tk.Tk()
    root.title("Interfaz PhantomX")
    logo_frame = ttk.Frame(root)
    logo_frame.grid(row=0, column=0, padx=10, pady=10)
    logo_image = Image.open(png_path)
    logo_image = logo_image.resize((150, 150), Image.ANTIALIAS) 
    logo_image = ImageTk.PhotoImage(logo_image)
    logo_label = ttk.Label(logo_frame, image=logo_image)
    logo_label.image = logo_image
    logo_label.grid(row=0, column=0, padx=10, pady=5)
    name_label = ttk.Label(logo_frame, text="Laboratorio 4 Robotica 2023-2S")
    name_label.grid(row=1, column=0, padx=10, pady=5)
    first_name_label = ttk.Label(logo_frame, text="Andres David Hernandez y Juan Sebastian Daleman")
    first_name_label.grid(row=2, column=0, padx=10, pady=5)
    second_name_label = ttk.Label(logo_frame, text="Pos1=[25 25 20 -20 0]\nPos2=[-35 35 -30 30 0]\nPos3=[85 -20 55 25 0]\nPos4=[80 -35 55 -45 0]")
    second_name_label.grid(row=3, column=0, padx=10, pady=5)
    buttons_frame = ttk.Frame(root)
    buttons_frame.grid(row=1, column=0, padx=10, pady=10)
    buttons = []
    button1 = ttk.Button(buttons_frame, text="Home", command=lambda i=1: button_click(i))
    button1.grid(row=0, column=0, padx=10, pady=5)
    buttons.append(button1)
    button2 = ttk.Button(buttons_frame, text="Posicion 1", command=lambda i=2: button_click(i))
    button2.grid(row=0, column=1, padx=10, pady=5)
    buttons.append(button2)
    button3 = ttk.Button(buttons_frame, text="Posicion 2", command=lambda i=3: button_click(i))
    button3.grid(row=0, column=2, padx=10, pady=5)
    buttons.append(button3)
    button4 = ttk.Button(buttons_frame, text="Posicion 3", command=lambda i=4: button_click(i))
    button4.grid(row=0, column=3, padx=10, pady=5)
    buttons.append(button4)
    button5 = ttk.Button(buttons_frame, text="Posicion 4", command=lambda i=5: button_click(i))
    button5.grid(row=0, column=4, padx=10, pady=5)
    buttons.append(button5)
    global text_box
    text_box = tk.Text(root, height=7, width=70)
    text_box.grid(row=2, column=0, padx=10, pady=10)
    root.mainloop()

if __name__ == '__main__':
    try:
        listener()
        ultPos=0
        rospack = rospkg.RosPack()
        package_path = rospack.get_path('dynamixel_one_motor')
        global png_path
        png_path = os.path.join(package_path, 'resources', 'unlogo.png')
        Nombres=["Waist","Shoulder","Elbow","Wrist","Hand"]
        PosHome=[512,512,512,512,512] # valores verificados en dynamixel wizard correspondientes a home
        pos1An=[598,598,580,444,512] # valores redondeados de dynamix wiz corresponidentes a posiciones dadas
        pos2An=[392,632,409,615,512]
        pos3An=[803,444,700,598,512]
        pos4An=[786,392,700,358,512]
        #posicion en grados
        posHomeDegree=[0,0,0,0,0]
        pos1Degree=[25,25,20,-20,0] 
        pos2Degree=[-35,35,-30,30,0]
        pos3Degree=[85,-20,55,25,0] 
        pos4Degree=[80,-35,55,-45,0]
        ListaPosiciones = [PosHome,pos1An,pos2An,pos3An,pos4An]
        ListaPosicionesDegree = [posHomeDegree,pos1Degree,pos2Degree,pos3Degree,pos4Degree]
        crearInterfaz()
    except rospy.ROSInterruptException:
        pass



