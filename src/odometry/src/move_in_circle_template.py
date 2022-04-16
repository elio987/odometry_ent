#!/usr/bin/env python
""" Implements a "ground truth" odometry using the model state information from Gazebo.
"""

import sys
import numpy as np
import rospy
from geometry_msgs.msg import Twist

class MoveInCircleCommander():
    def __init__(self):

        rospy.init_node('MoveInCircle')

        # Publish to the /cmd_vel topic
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.rate = rospy.Rate(20)


    def main(self, radie=1.2, linvel=0.1 ):

        # If there's an object attached to the ee we want it to follow its trajectory
        while not rospy.is_shutdown():
            self.rate.sleep()

            self._move_in_circle(radie, linvel)


    def _move_in_circle(self, radie, linvel):

        tw = Twist()
        tw.linear.x = 0.1
        tw.linear.y = 0.0
        tw.linear.z = 0.0
        tw.angular.x = 0.0
        tw.angular.y = 0.0
        tw.angular.z = -0.0833
        #----------------------------------------------------------------------------
        # Your code here

        #----------------------------------------------------------------------------

        self.pub.publish(tw)



if __name__ == '__main__':

    try:
        node = MoveInCircleCommander()
        if len(sys.argv) >= 3:
            node.main(radie=sys.argv[1], linvel=sys.argv[2])
        else:
            node.main()
    except (rospy.ROSInterruptException, rospy.ROSException("topic was closed during publish()")):
        pass
