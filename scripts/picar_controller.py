#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from SunFounder_PiCar import front_wheels
from SunFounder_PiCar import back_wheels

import SunFounder_PiCar
import time
import math

SunFounder_PiCar.setup()

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
fw.turning_max = 30

forward_speed = 50
backward_speed = 50

def callback(msg):

    rospy.loginfo(rospy.get_caller_id() + "Twist %s", msg)

    if(msg.linear.x > 0.1):
	bw.forward()
	bw.speed = int(100 * msg.linear.x)
    elif(msg.linear.x < -0.1):
	bw.backward()
	bw.speed = int(100 * -msg.linear.x)
    else:
	bw.stop()

    if(msg.angular.z > 0.1 or msg.angular.z < -0.1):
	fw.turn( int(90 - 20 * msg.angular.z) )
    else:
	fw.turn_straight()

def picar_controller():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('picar_controller', anonymous=False)

    rospy.Subscriber("cmd_vel", Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

def stop():
    rospy.loginfo("STOP")
    bw.stop()
    fw.turn_straight()

if __name__ == '__main__':
    try:
	picar_controller()
    except KeyboardInterrupt:
        print "KeyboardInterrupt, motor stop"
        stop()
    except rospy.ROSInterruptException:
	stop()
	pass
    finally:
	stop()
