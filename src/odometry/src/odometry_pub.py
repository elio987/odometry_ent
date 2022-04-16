#!/usr/bin/env python
# coding=utf-8
import numpy as np
import rospy
from nav_msgs.msg import Odometry
import tf2_ros
from geometry_msgs.msg import TransformStamped,PoseWithCovariance,TwistWithCovariance
from std_msgs.msg import Float32

class OdometryCal():
    def __init__(self):
        #Inicializamos el nodo
        rospy.init_node("odometry_pub")
        #Creamos las variables que van a contener los valores de los subscribers
        self.wr = 0
        self.wl = 0
        self.th = 0.0
        #Creamos los susbcribers
        rospy.Subscriber("/wr",Float32,self.wr_callback)
        rospy.Subscriber("/wl",Float32,self.wl_callback)
        #Creamos los publishers
        self.pub_odom = rospy.Publisher("/odometry", Odometry, queue_size=1)
        #Iniciamos el voctor de posición en cero
        self.pos = np.array([[0.0],[0.0],[0.0]])
        #Declaramos que vamos a mandar 20 mensajes por segundo
        self.rate = rospy.Rate(3000)
    #Las funciones callback para extraer los datos de los susbcribers
    def wr_callback(self,w):
        self.wr = w.data
    def wl_callback(self,w):
        self.wl = w.data
    #Calculamos la odometria estimada en forma de vector
    def odometry_cal(self,dt,v,w):
        """Funcion para hacer el claculo del nuevo vector de odometria a lo largo del tiempo"""
        y_k = self.pos
        #Si el diferencialde tiempo es muy grande ignoramos esa iteracion
        if dt < 1:
            #Calculamos el nuevo vector de posicion
            y_k1 = y_k + (np.array([[w],[v*np.cos(y_k[0,0])],[v*np.sin(y_k[0,0])]]))*dt
            #print(dt)
        else:
            y_k1 = y_k
        #cuando el angulo de inclinacion de una vuelta completa lo reiniciamos
        if y_k1[0,0] < -2*np.pi:
            y_k1[0,0] = 0.0
        #Hacemos el refresh
        self.pos = y_k1
        return self.pos

    def main(self):
        #Obtenemos el tiempo inicial
        t0 = rospy.get_rostime().to_sec()
        while not rospy.is_shutdown():
            #Calculamos la velocidad lineal y angular
            w = 0.05*((self.wr-self.wl)/0.191)
            v = 0.05*((self.wr+self.wl)/2)
            #print(v,w)
            #Obtenemos el tiempo final
            tf = rospy.get_rostime().to_sec()
            #odometria calculada
            y_k = self.odometry_cal(tf-t0,v,w)
            print("calculado",y_k)
            #Publicamos lo nuevos valores de odometria
            msg_odom = Odometry()
            msg_odom.header.stamp = rospy.Time.now()
            msg_odom.header.frame_id = "odometria_msg"
            msg_odom.pose.pose.orientation.z = y_k[0,0]
            msg_odom.pose.pose.position.x = y_k[1,0]
            msg_odom.pose.pose.position.y = y_k[2,0]
            self.pub_odom.publish(msg_odom)
            #Hacemos el sleep para asegurar los 20 mensajes por segundo.
            self.rate.sleep()
            #Actualizamos el tiempo
            t0 = tf
#Si el archivo es corrido directametne y no llamado desde otro archivo corremos
if __name__ == "__main__":
    #iniciamos la clase
    odom_mov = OdometryCal()
    #Corremos la funcion principal
    odom_mov.main()
