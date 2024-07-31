import rospy
import numpy as np
import apriltag
import serial
import datetime
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

arduino = serial.Serial(port='/dev/ttyACM0',   baudrate=9600)

def callback(msg):
    aX = msg[0]
    aY = msg[1]

    elapsed_time_ms = (datetime.datetime.now() - ot).total_seconds() * 1000
    rate = 10 # frames per second
    if elapsed_time_ms > 1000/rate:
        coordinates = f"{aX},{aY}\r"
        arduino.write(coordinates.encode())
        print(ot, elapsed_time_ms)
        ot = datetime.datetime.now()

def subscriber():
    rospy.init_node('processor', anonymous=True)
    rospy.Subscriber('/photo', Image, callback) 
    pub = rospy.Publisher('process', Image, queue_size=10)
    rospy.spin()