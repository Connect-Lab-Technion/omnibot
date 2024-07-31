import cv2
import numpy as np
from apriltag import apriltag

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = img.float() / 255.0
    img = img.permute(2, 0, 1).unsqueeze(0)
detector = apriltag("tagStandard41h12")

detections = detector.detect(img)

for a in detections:
    (ptA, ptB, ptC, ptD) = a.corners
    ptA = (int(ptA[0]), int(ptA[1]))
    ptB = (int(ptB[0]), int(ptB[1]))
    ptC = (int(ptC[0]), int(ptC[1]))
    ptD = (int(ptD[0]), int(ptD[1]))

    cv2.line(img, ptA, ptB, (0, 255, 0), 2)
    cv2.line(img, ptB, ptC, (0, 255, 0), 2)
    cv2.line(img, ptC, ptD, (0, 255, 0), 2)
    cv2.line(img, ptD, ptA, (0, 255, 0), 2)

    (cX, cY) = (int(a.center[0]), int(a.center[1]))
    cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)

    tagFamily = a.tag_family.decode("utf-8")
    cv2.putText(img, tagFamily, (ptA[0], ptA[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('YOLOv7 Webcam Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()