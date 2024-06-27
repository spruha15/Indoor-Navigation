#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time 

def rotate90():
    cmd = Twist()
    cmd.angular.z = 2
    current_angle = 0
    t0 = rospy.Time.now().to_sec
    while current_angle< (math.pi/2):
        pub.publish(cmd)
        t1 = rospy.Time.now().to_sec
        current_angle = (cmd.angular.z)*(t1-t0)
        rate = rospy.Rate(4)
        rate.sleep()
    cmd.angular.z = 0
    pub.publish(cmd)    


def spiral(pose: Pose):
    cmd = Twist()
    vk = 1
    wk = 2
    rk = 0.5
    constant_velocity = 4
    rate = rospy.Rate(1)

    while (pose.x<7.0) and (pose.y<7.0):
        rk = rk + 0.5
        cmd.linear.x = rk
        #cmd.angular.z = constant_velocity
        pub.publish(cmd)
        rate.sleep()
        rotate90()
        rate.sleep()

    cmd.linear.x = 0.0
    pub.publish(cmd) 


if __name__ == '__main__':

    rospy.init_node('square')
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10) 
    sub = rospy.Subscriber("/turtle1/pose",Pose,callback= spiral)
    rospy.spin()