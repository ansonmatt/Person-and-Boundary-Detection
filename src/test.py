from ultralytics import YOLO
model = YOLO("yolov8n.pt")
print("YOLOv8 ready")

import supervision as sv
print("Supervision ready")

import cv2
print("OpenCV ready")

print("All good!")
