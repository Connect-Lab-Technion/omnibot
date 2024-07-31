import cv2
import numpy as np
import apriltag
import serial
import datetime

cap = cv2.VideoCapture(0)

arduino = serial.Serial(port='/dev/ttyACM0',   baudrate=9600)

detector = apriltag.Detector(options=apriltag.DetectorOptions(families="tag36h11"))

ot = datetime.datetime.now()
numDetections = 0
numDetections2= 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = detector.detect(img)

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

        elapsed_time_ms = (datetime.datetime.now() - ot).total_seconds() * 1000
        rate = 10 # frames per second
        if elapsed_time_ms > 1000/rate:
            coordinates = f"{aX},{aY}\r"
            arduino.write(coordinates.encode())
            print(ot, elapsed_time_ms)
            ot = datetime.datetime.now()

    cv2.imshow('apriltag detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()