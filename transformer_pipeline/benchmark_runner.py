import time
import cv2
import csv
from ultralytics import YOLO

# 1. Load your custom trained YOLOv8 model (update file name if needed)
print("Initializing Custom-Trained YOLOv8 Nano on Laptop CPU...")
model = YOLO("best.pt") 

# 2. Path to your test video file
video_path = r"C:\Users\Ann\boundary_detection\videos\test4.mp4" 
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file at '{video_path}'")
    exit()

print("\n--- STARTING LOCAL YOLO BENCHMARK (150 Frames) ---")
frame_count = 0
total_inference_time = 0

while cap.isOpened() and frame_count < 150:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame_count += 1
    start_time = time.time()
    
    # Run prediction locally on CPU
    results = model.predict(frame, classes=[0], save=False, verbose=False)
    
    end_time = time.time()
    total_inference_time += (end_time - start_time)

cap.release()

average_local_fps = frame_count / total_inference_time
print(f"--- BENCHMARK COMPLETE ---")
print(f"Processed {frame_count} frames on local CPU.")
print(f"Average Local YOLO Speed: {average_local_fps:.1f} FPS")

# 3. Save the findings to a comparative log file
log_path = "transformer_pipeline/comparative_log.csv"
with open(log_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Model Architecture", "Hardware Platform", "Compute Unit", "Throughput Speed (FPS)"])
    writer.writerow(["YOLOv8 Nano (Custom)", "Local Laptop", "CPU", f"{average_local_fps:.1f}"])
    writer.writerow(["RT-DETR Large (Vanilla)", "Google Colab", "T4 Cloud GPU", "9.1"])

print(f"Metrics saved cleanly to: {log_path}")