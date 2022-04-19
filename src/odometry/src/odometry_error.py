#!/usr/bin/env python
# coding=utf-8
import numpy as np
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from tf.transformations import euler_from_quaternion, quaternion_matrix
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
            #extraemos los tres angulos
            x,y,z = ang
            #Hacmos que el angulo obtenido sea siempre positivo y llegue hasta los 2pi
            if z > 0.0:
                z = z - 2*np.pi
            #Aqui obtenemos la rotacion de la odometria real a la calculada
            #matriz de rotacion odometria real
            R_sr = np.array([[np.cos(z),-1*np.sin(z),0],
                              [np.sin(z),np.cos(z),0],
                              [0,0,1]])
            #Traslacion odometria real
            d_sr = np.array([[self.true_odometry[1]],
                             [self.true_odometry[2]],
                             [0]])
            #Matriz de rotacion odoemtria calculada
            R_sc = np.array([[np.cos(self.odometry[0]),-1*np.sin(self.odometry[0]),0],
                              [np.sin(self.odometry[0]),np.cos(self.odometry[0]),0],
                              [0,0,1]])
            #Traslacion odometria calculada
            d_sc = np.array([[self.odometry[1]],
                             [self.odometry[2]],
                             [0]])
            #Matriz de rotacion de la odometria real a la calculada
            R = np.dot(R_sr.T,R_sc)
            #Traslacion de la real a la calculada
            d = np.dot(R_sr.T,d_sc-d_sr)
            #Obtenemos el angulo de rotacion
            angulo_er = np.arctan2(R[1,0],R[0,0])
            #Plotemos la posicion
            pos_x.append(self.odometry[1])
            pos_y.append(self.odometry[2])
            pos_x_t.append(self.true_odometry[1])
            pos_y_t.append(self.true_odometry[2])
            plt.plot(pos_x,pos_y)
            plt.plot(pos_x_t,pos_y_t)
            plt.legend(["odometria calculada","odometria real"])
            plt.draw()
            plt.pause(0.00001)
            plt.clf()
            #Publicamos los valores obtenidos
            self.pub_ang_err.publish(angulo_er)
            self.pub_posx_err.publish(d[0,0])
            self.pub_posy_err.publish(d[1,0])
            #Usamos el sleep para pode asegurar los 20 msg por segundo.
            self.rate.sleep()
#Si el archivo es corrido directametne y no llamado desde otro archivo corremos
if __name__ == "__main__":
    #Iniciamos la clase
    odo_err = OdometryError()
    #Llamamos la funcion principal
    odo_err.main()
