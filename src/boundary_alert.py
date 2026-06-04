import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

# ==========================================
# CONFIGURATION ZONE (Update these for each new video)
# ==========================================
VIDEO_PATH = "videos/test.mp4"
MODEL_PATH = "best.pt" # Or yolov8n.pt if starting completely fresh

# YOLO Inference Settings (optimized for accuracy)
YOLO_IMG_SIZE = 640  # Increased from 480 for better detection of distant/small people
YOLO_NMS_CONF = 0.45  # NMS threshold to reduce overlapping detections
YOLO_DEFAULT_CONF = 0.4  # Default confidence threshold (40%)

# Paste your Red Alarm Zone coordinates here
ALARM_POLYGON = np.array([
    [900, 400],   # Top-left (was 600)
    [1500, 400],  # Top-right (was 600)
    [1500, 800],  # Bottom-right (was 1000)
    [900, 800]    # Bottom-left (was 1000)
])

# Paste any Blue Exclusion Zones here (to hide static poles/lights). 
# Leave the list empty [] if the new video has no false alarms!
EXCLUSION_ZONES_RAW = [
    # np.array([[X, Y], [X, Y], [X, Y], [X, Y]]), # Example Zone 1
]
# ==========================================

# 1. Initialize Model and Video
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_PATH)

# 2. Initialize Supervision Tools
zone = sv.PolygonZone(polygon=ALARM_POLYGON)
zone_annotator = sv.PolygonZoneAnnotator(zone=zone, color=sv.Color.RED)
box_annotator = sv.BoxAnnotator()

# Initialize Exclusion Zones (if any exist)
exclusion_zones = [sv.PolygonZone(polygon=p) for p in EXCLUSION_ZONES_RAW]
exclusion_annotators = [sv.PolygonZoneAnnotator(zone=z, color=sv.Color.BLUE) for z in exclusion_zones]

print("Starting Universal Boundary Detection Engine...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Run YOLO with optimized parameters
    results = model(frame, conf=YOLO_DEFAULT_CONF, imgsz=YOLO_IMG_SIZE, iou=YOLO_NMS_CONF)[0]
    detections = sv.Detections.from_ultralytics(results)
    
    # Keep ONLY 'Person' (class_id 0)
    detections = detections[detections.class_id == 0]
    
    # 3a. FILTER: Remove tiny detections (likely false positives)
    if len(detections) > 0:
        widths = detections.xyxy[:, 2] - detections.xyxy[:, 0]
        heights = detections.xyxy[:, 3] - detections.xyxy[:, 1]
        min_size = 20  # Minimum bounding box width/height in pixels
        valid_size = (widths >= min_size) & (heights >= min_size)
        detections = detections[valid_size]
    
    # 4. FILTER: Smart Exclusion Zones (The "Count Increase" Logic)
    if exclusion_zones:
        keep_mask = np.ones(len(detections), dtype=bool)
        for excl_zone in exclusion_zones:
            in_this_zone = excl_zone.trigger(detections=detections)
            current_count = np.sum(in_this_zone)
            
            # If only 1 object is in the blue zone, assume it's the static pole.
            if current_count == 1:
                keep_mask[in_this_zone] = False
                
        detections = detections[keep_mask]

    # 5. ALARM LOGIC
    is_inside = zone.trigger(detections=detections)
    if is_inside.any():  
        cv2.putText(frame, "ALERT: ZONE BREACH", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # 6. Draw Annotations
    frame = box_annotator.annotate(scene=frame, detections=detections)
    frame = zone_annotator.annotate(scene=frame)
    for annotator in exclusion_annotators:
        frame = annotator.annotate(scene=frame)
    
    # 7. Display Live Feed
    cv2.imshow("Security Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
