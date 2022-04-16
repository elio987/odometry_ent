#!/usr/bin/env python
# coding=utf-8
import sys
import numpy as np
import rospy
from geometry_msgs.msg import Twist
#Creamos la clase
class MovimientoCirculo():
    def __init__(self):
        #Inicializamos el nodo
        rospy.init_node("circulo_mov")
        #Creamos el publisher
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        #Declaramos que vamos a mandar 20 mensajes por segundo.
        self.rate = rospy.Rate(3000)
        #Creamos el msg Twist
        self.msg = Twist()
        #Creamos un función de que hacer cuando haya un shutdown
        rospy.on_shutdown(self.end_callback)
    def mover_en_circulo(self,v_lin,v_ang):
        """Funcion que publica la velocidad lineal y angular en el puzzlebot"""
        #Declaramos le velocidad deseada en el mensaje tipo Twist
        self.msg.linear.x = v_lin
        self.msg.linear.y = 0.0
        self.msg.linear.z = 0.0
        self.msg.angular.x = 0.0
        self.msg.angular.y = 0.0
        self.msg.angular.z = v_ang
        #Publicamos la velocidad
        self.pub.publish(self.msg)
    def end_callback(self):
        """Funcion que para el puzzlebot cuando el nodo deja de ser corrido"""
        #Declaramos las velocidades de cero
    	self.msg.linear.x = 0.0
    	self.msg.angular.z = 0.0
        #Publicamos las velocidades
    	self.pub.publish(self.msg)
#Si el archivo es corrido directametne y no llamado desde otro archivo corremos
if __name__ == "__main__":
    #iniciamos la clase
    mov = MovimientoCirculo()
    #mientras este corriendo el nodo movemos el carro el circulo
    while not rospy.is_shutdown():
        #Llamamos el sleep para asegurar los 20 msg por segundo
        mov.rate.sleep()
        mov.mover_en_circulo(0.1,-0.08333333333)
    #mov.main()
