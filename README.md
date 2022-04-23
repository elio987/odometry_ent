# odometria_ent

1. El nodo que publica en el tópico /cmd_vel para hacer que se mueve el puzzlebot en forma de un círculo con radie 1.2m y con velocidad lineal de 0.1 m/s se implementó en el archivo /src/odometry/src/circulo_mov.py

2. El nodo que publica la odometría en el tópico /odometry usando las velocidades de ambas ruedas del puzzlebot se implementó en el archivo /src/odometry/src/odometry_pub.py

3. El nodo que se subscribe a los dos tópicos /odometry y /true_odometry, calcula el error entre los valores de la odometría real con la calculada y lo publica en los tópicos /odometry_error/pose/x, /odometry_error/pose/y y /odometry_error/pose/angle, se implementó  en el archivo /src/odometry/src/odometry_error.py

4. Además de crear un archivo launch que corra todos los nodos necesarios al mismo timepo, llamado odometry_launch.launch, se implemento en el archivo /src/odometry/launch/odomentry_launch.launch

- Para poder correr todo ingresamos los siguientes comandos en una terminal diferente:
```
	roscore
	roslaunch puzzlebot_gazebo puzzlebot_gazebo.launch
	roslaunch odometry odometry_launch.launch
	rqt_plot /odometry_error/pose/x:y:angle
```
