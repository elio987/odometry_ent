#!/usr/bin/env python
# coding=utf-8
import numpy as np
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion
import matplotlib.pyplot as plt
#Creamos la clase
class OdometryError():
    def __init__(self):
        #Inicializamos el nodo
        rospy.init_node("odometry_error")
        #Cremos los vectores de posision para la odometria real y estimada.
        self.odometry = [0.0,0.0,0.0]
        self.true_odometry = [0.0,0.0,0.0]
        #Creamos los susbcribers
        rospy.Subscriber("/odometry",Odometry,self.odometry_callback)
        rospy.Subscriber("/true_odometry",Odometry,self.true_odometry_callback)
        #Creamos los publishers
        self.pub_posx_err = rospy.Publisher("/odometry_error/pose/x", Float64, queue_size=1)
        self.pub_posy_err = rospy.Publisher("/odometry_error/pose/y", Float64, queue_size=1)
        self.pub_ang_err = rospy.Publisher("/odometry_error/pose/angle", Float64, queue_size=1)
        #Declaramos 20 msg por segundo
        self.rate = rospy.Rate(3000)
    #Creamos lo callbacks para poder extraer los datos de los subscribers
    def odometry_callback(self,data):
        header = data.header.stamp
        pose = data.pose
        self.odometry = [pose.pose.orientation.z,pose.pose.position.x,pose.pose.position.y]
    def true_odometry_callback(self,data):
        header = data.header.stamp
        pose = data.pose
        #Como el de la odometria real esta en un cuaternion usamos la sigueinte funcion para extraer su angulo de inclinacion en el eje z
        self.true_odometry = [euler_from_quaternion([pose.pose.orientation.x,pose.pose.orientation.y,
        pose.pose.orientation.z,pose.pose.orientation.w]),pose.pose.position.x,pose.pose.position.y]
    def main(self):
        #Mientras el nodo este corriendo
        pos_x = []
        pos_y = []
        pos_x_t = []
        pos_y_t = []
        while not rospy.is_shutdown():
            ang = self.true_odometry[0]
            #Si el valor obtenido no es una tupla ignoramos esta iteracion
            if type(ang) == float:
                continue
            #print(type(ang))
            #extraemos los tres angulos
            x,y,z = ang
            #Hacmos que el angulo obtenido sea siempre positivo y llegue hasta los 2pi
            if z > 0.0:
                z = z - 2*np.pi
            #print(self.odometry)
            #Aqui restamos los valores de la odometria real con la calculada y publicamos sus valores.
            error_ang = Float64()
            error_ang.data = abs(z - self.odometry[0])
            self.pub_ang_err.publish(error_ang)
            error_posex = Float64()
            error_posey = Float64()
            error_posex.data = abs(self.true_odometry[1] - self.odometry[1])
            error_posey.data = abs(self.true_odometry[2] - self.odometry[2])
            #Ploteamos la posicion de las dos odometrias en x y
            pos_x.append(self.odometry[1])
            pos_y.append(self.odometry[2])
            pos_x_t.append(self.true_odometry[1])
            pos_y_t.append(self.true_odometry[2])
            plt.plot(pos_x,pos_y)
            plt.plot(pos_x_t,pos_y_t)
            plt.legend(["odometria calculada","odometria real"])
            plt.draw()
            plt.pause(0.0001)
            plt.clf()
            self.pub_posx_err.publish(error_posex)
            self.pub_posy_err.publish(error_posey)
            #Usamos el sleep para pode asegurar los 20 msg por segundo.
            self.rate.sleep()
#Si el archivo es corrido directametne y no llamado desde otro archivo corremos
if __name__ == "__main__":
    #Iniciamos la clase
    odo_err = OdometryError()
    #Llamamos la funcion principal
    odo_err.main()
