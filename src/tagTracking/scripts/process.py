#!/usr/bin/env python3.9

import rospy
import cv2
import numpy as np
import apriltag
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

detector = apriltag.Detector(options=apriltag.DetectorOptions(families="tag36h11"))

def callback(msg):
    #recieve image
    bridge = CvBridge()
    current_frame = bridge.imgmsg_to_cv2(msg)

    processedImage = imageProcessor(msg)
    #publish image
    global pub
    rospy.init_node('camera', anonymous=True)
    pub = rospy.Publisher('photo', Image, queue_size=10)

    if processedImage is not None:
        rospy.loginfo("Publishing image")
        pub.publish(processedImage)

def subscriber():
    rospy.init_node('processor', anonymous=True)
    rospy.Subscriber('/photo', Image, callback) 
    pub = rospy.Publisher('process', Image, queue_size=10)
    rospy.spin()

def imageProcessor(frame):
    
    detections = detector.detect(frame)

    sX = 0
    sY = 0
    
    for a in detections:
        (ptA, ptB, ptC, ptD) = a.corners.astype(int)
        ptA = tuple(ptA)
        ptB = tuple(ptB)
        ptC = tuple(ptC)
        ptD = tuple(ptD)

        cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
        cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
        cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
        cv2.line(frame, ptD, ptA, (0, 255, 0), 2)

        (cX, cY) = tuple(map(int, a.center))
        cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

        depth = apriltag.depth(ptA, ptB, ptC, ptD)
        
        cv2.putText(frame, f"{depth:.1f}", (ptA[0], ptA[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        sX += cX
        sY += cY
        
    if len(detections) > 0:
        numDetections +=1
        numDetections2 += len(detections)
        print(numDetections, numDetections2)
        aX = sX//len(detections)
        aY = sY//len(detections)
        cv2.circle(frame, (aX, aY), 5, (0, 0, 255), -1)

    coords = tuple(aX, aY)
    if coords is not None:
        rospy.loginfo("Publishing image")
        pub.publish(coords)

def publisher():
    global pub
    rospy.init_node('camera', anonymous=True)
    pub = rospy.Publisher('/photo', Image, queue_size=10)

    # Set up a timer to call `publish_image` every 0.1 seconds
    rospy.Timer(rospy.Duration(0.1), lambda event: imageProcessor(event, pub))

    rospy.spin()

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass