import rospy
from sensor_msgs.msg import Range


TRIG = 11
ECHO = 12


def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100


def ultrasonic():

    GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

    rospy.init_node('ultrasonic_publisher', anonymous=False)
    rospy.on_shutdown(cleanup)
    pub = rospy.Publisher('range', Range, queue_size=50)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        range_msg = Range()
        range_msg.radiation_type = range.ULTRASOUND;
        range_msg.header.frame_id =  'range_frame';
        range_msg.header.stamp =  rospy.Time.now();
        range_msg.field_of_view = 0.1; 
        range_msg.min_range = 0.0;
        range_msg.max_range = 100.0;
        range_msg.range =  distance()

        pub.publish(range_msg)
        rate.sleep()



def cleanup():
    print "Shutting down HC-SR04"
	GPIO.cleanup()


if __name__ == '__main__':
    try:
        ultrasonic()
    except rospy.ROSInterruptException:
        pass