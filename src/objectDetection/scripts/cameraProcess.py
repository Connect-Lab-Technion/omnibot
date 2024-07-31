#!/usr/bin/env python3.9

import rospy
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '/home/connect/yolo7'))

import cv2
import torch
from yolov7.models.experimental import attempt_load
from yolov7.utils.general import non_max_suppression, scale_coords
from yolov7.utils.plots import plot_one_box
from yolov7.utils.torch_utils import select_device
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

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
    # Add YOLOv7 directory to the path
    sys.path.append(os.path.join(os.getcwd(), 'yolov7'))

    # Initialize YOLOv7 model
    device = select_device('')  # Use '0' for GPU or '' for CPU
    model = attempt_load('yolov7/yolov7.pt', map_location=device)
    model.eval()

    img = frame
    img = torch.from_numpy(img).to(device)
    img = img.float() / 255.0
    img = img.permute(2, 0, 1).unsqueeze(0)

    # Run YOLOv7 inference
    with torch.no_grad():
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.4, 0.5)  # Adjust confidence and NMS thresholds

    # Process detections
    for det in pred:
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

            for *xyxy, conf, cls in det:
                label = f'{cls}: {conf:.2f}'
                plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)

    return img #wrong needs fixed

if __name__ == '__main__':
    try:
        subscriber()
    except rospy.ROSInterruptException:
        pass