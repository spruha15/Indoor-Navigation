#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time



def pose_callback(pose):
    global x
    global y
    global yaw 

    yaw = pose.theta
    x = pose.x
    y = pose.y



def move(speed,distance,is_forward):
    cmd = Twist()
    global x,y
    x0 = x
    y0 = y

    if(is_forward):
        cmd.linear.x = abs(speed)
    else:
        cmd.linear.x = -abs(speed)

    distance_moved = 0
    rate = rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)      

    while True :
        pub.publish(cmd)
        rate.sleep()


        distance_moved = distance_moved + abs( math.sqrt(((x-x0)**2)+ ((y-y0)**2)))

        if not (distance_moved<distance):
            rospy.loginfo('reached')
            break
    cmd.linear.x = 0
    pub.publish(cmd)
    rotate(90,30,False)
    move(3.0,8.0,True)


def rotate(ang_velocity,rel_angle,clockwise):
    global yaw

    cmd = Twist()


    theta0 = yaw
    ang_speed = math.radians(abs(ang_velocity))

    if (clockwise):
        cmd.angular.z = -abs(ang_speed)
    else:
        cmd.angular.z = abs(ang_speed)

    ang_speed = 0.0
    rate = rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    
    t0 = rospy.Time.now().to_sec()

    while True:
        pub.publish(cmd)
        

        t1 = rospy.Time.now().to_sec()
        current_angle = (t1-t0)* ang_speed
        rate.sleep()


        if (current_angle<rel_angle):
            break

    cmd.angular.z = 0.0
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
    




def spiral(pose: Pose):
    global x
    global y

    cmd = Twist()

    count = 0
    vk = 1
    wk = 2
    rk = 0.5
    constant_velocity = 4
    rate = rospy.Rate(1)

    while (pose.x<9.0) and (pose.y<9.0):
        rk = rk + 0.5
        cmd.linear.x = rk
        cmd.angular.z = constant_velocity
        pub.publish(cmd)
        rate.sleep()
    cmd.linear.x = 0.0
    pub.publish(cmd)


def rotate90():
    cmd = Twist()
    cmd.angular.z = 2
    current_angle = 0
    t0 = rospy.Time.now().to_sec
    while current_angle< (math.pi):
        pub.publish(cmd)
        t1 = rospy.Time.now().to_sec
        current_angle = 2*(t1-t0)
        rate = rospy.Rate(200)
        rate.sleep()
    cmd.angular.z = 0
    pub.publish(cmd)    

def square():
    count = 0
    while count<4:
        #move(3.0,8.0,True)
        rotate90()
        count+=1


def go_to_goal(x_goal,y_goal):
    global x
    global y 
    cmd = Twist

    while(True):
        k_linear = 0.5
        distance = abs(math.sqrt(((x_goal-x)**2)+ ((y_goal-y)**2)))

        linear_speed = distance*k_linear

        k_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y,x_goal-x)
        angular_speed = (desired_angle_goal-yaw)*k_angular

        cmd.linear.x = linear_speed
        cmd.angular.z = angular_speed
        pub.publish(cmd)


        if (distance<0.01):
            break




        





if __name__ == '__main__':

    rospy.init_node('square')
    pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10) 
    sub = rospy.Subscriber("/turtle1/pose",Pose,callback= pose_callback)
    time.sleep(10)

    #rotate(90,30,False)
    #move(3.0,8.0,True)
    #spiral(Pose)
    #square()
    #rotate90()
    #go_to_goal(1.0,1.0)


    

    

    





        





    
        
   
    

   
    
    

    
   