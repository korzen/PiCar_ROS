#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from SunFounder_PiCar import front_wheels
from SunFounder_PiCar import back_wheels

import SunFounder_PiCar

SunFounder_PiCar.setup()

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
fw.turning_max = 45

forward_speed = 70
backward_speed = 70

def callback(twist):
   # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    rospy.loginfo(rospy.get_caller_id() + "I heard Twist %s", twist)

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
    except rospy.ROSInterruptException:
	stop()
	pass

