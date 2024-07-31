#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

def capture_image():
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        rospy.logerr("Error: Could not open video capture.")
        return None
    
    ret, frame = cap.read()
    if ret:
        # Convert the image to RGB format
        bridge = CvBridge()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        jpeg_data = bridge.cv2_to_imgmsg(img, encoding="mono8")
        cap.release()  # Release the camera
        return jpeg_data
    else:
        rospy.logerr("Error: Could not capture image.")
        cap.release()  # Release the camera
        return None

def publish_image(event, pub):
    jpeg_data = capture_image()

    if jpeg_data is not None:
        rospy.loginfo("Publishing image")
        pub.publish(jpeg_data)

def publisher():
    global pub
    rospy.init_node('camera', anonymous=True)
    pub = rospy.Publisher('/photo', Image, queue_size=10)

    # Set up a timer to call `publish_image` every 0.1 seconds
    rospy.Timer(rospy.Duration(0.1), lambda event: publish_image(event, pub))

    rospy.spin()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass