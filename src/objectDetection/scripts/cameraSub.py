#!/usr/bin/env python

import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class VideoSaver:
    def __init__(self, filename, codec='mp4v', fps=10):
        self.video_writer = None
        self.filename = filename
        self.codec = codec
        self.fps = fps
        self.is_initialized = False

    def initialize_writer(self, frame):
        height, width, _ = frame.shape
        self.video_writer = cv2.VideoWriter(
            self.filename,
            cv2.VideoWriter_fourcc(*self.codec),
            self.fps,
            (width, height)
        )
        self.is_initialized = True

    def write_frame(self, frame):
        if not self.is_initialized:
            self.initialize_writer(frame)
        self.video_writer.write(frame)

    def release(self):
        if self.video_writer is not None:
            self.video_writer.release()

def callback(msg):
    bridge = CvBridge()
    current_frame = bridge.imgmsg_to_cv2(msg)
    video_saver.write_frame(current_frame)

def subscriber():
    global video_saver
    rospy.init_node('subscriber', anonymous=True)
    rospy.Subscriber('/process', Image, callback) 
    rospy.spin()

if __name__ == '__main__':
    video_saver = VideoSaver('./routine.mp4')
    try:
        subscriber()
    finally:
        video_saver.release()