import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ==========================================
# CONFIGURATION ZONE
# ==========================================
VIDEO_PATH = "videos/test4.mp4"
MODEL_PATH = "best.pt"

# YOLO Inference Settings (optimized for accuracy)
YOLO_IMG_SIZE = 640  # Increased from 480 for better detection of distant/small people
YOLO_NMS_CONF = 0.45  # NMS threshold to reduce overlapping detections
YOLO_DEFAULT_CONF = 40  # Better default confidence threshold

ALARM_POLYGON = np.array([
    [725, 852],
    [956, 760],
    [1169, 798],
    [948, 931],
])

# Paste your blue exclusion zones here if you have them
EXCLUSION_ZONES_RAW = [] 
# ==========================================

class SecurityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Security Dashboard")
        self.root.geometry("1000x750")
        
        # 1. Initialize AI and Video
        print("Loading AI Model...")
        self.model = YOLO(MODEL_PATH)
        self.cap = cv2.VideoCapture(VIDEO_PATH)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not load video feed.")
            self.root.quit()

        # 2. Setup Supervision Tools 
        self.zone = sv.PolygonZone(polygon=ALARM_POLYGON)
        self.zone_annotator = sv.PolygonZoneAnnotator(zone=self.zone, color=sv.Color.RED)
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator(text_color=sv.Color.BLACK) 
        
        # --- BYTETRACK & PATH TRACING ---
        self.tracker = sv.ByteTrack()  
        self.trace_annotator = sv.TraceAnnotator(thickness=2, trace_length=60)
        
        self.exclusion_zones = [sv.PolygonZone(polygon=p) for p in EXCLUSION_ZONES_RAW]
        self.excl_annotators = [sv.PolygonZoneAnnotator(zone=z, color=sv.Color.BLUE) for z in self.exclusion_zones]

        # 3. Build the UI (Dark Mode Theme)
        self.root.configure(bg="#121212") 

        # Title
        self.title_label = tk.Label(root, text="🛡️ AI PERIMETER SECURITY", 
                                    font=("Consolas", 18, "bold"), 
                                    bg="#121212", fg="#00FF41")
        self.title_label.pack(pady=15)

        # Video Canvas
        self.video_canvas = tk.Canvas(root, width=960, height=540, bg="black", 
                                      highlightthickness=2, highlightbackground="#333333")
        self.video_canvas.pack()

        # Control Panel Frame
        self.control_frame = tk.Frame(root, bg="#121212")
        self.control_frame.pack(pady=20, fill=tk.X, padx=50)

        # Total Count Label
        self.count_label = tk.Label(self.control_frame, text="Total People: 0", 
                                    font=("Consolas", 14, "bold"), bg="#121212", fg="#00FF41")
        self.count_label.pack(side=tk.LEFT, padx=20)

        # Live Confidence Slider 
        self.slider_label = tk.Label(self.control_frame, text="AI Confidence:", 
                                     font=("Consolas", 12), bg="#121212", fg="white")
        self.slider_label.pack(side=tk.LEFT, padx=10)

        self.conf_var = tk.IntVar(value=YOLO_DEFAULT_CONF) 
        self.conf_slider = tk.Scale(self.control_frame, from_=10, to=90, orient=tk.HORIZONTAL, 
                                    bg="#252526", fg="white", highlightthickness=0, length=200,
                                    variable=self.conf_var) 
        self.conf_slider.pack(side=tk.LEFT, padx=10)

        # Quit Button
        self.btn_quit = tk.Button(self.control_frame, text="SHUTDOWN", font=("Consolas", 12, "bold"), 
                                  bg="#D32F2F", fg="white", activebackground="#B71C1C", 
                                  relief=tk.FLAT, padx=20, command=self.quit_app)
        self.btn_quit.pack(side=tk.RIGHT, padx=10)

        # 4. State tracking & Start Loop
        self.frame_count = 0
        self.last_detections = None
        self.unique_people_in_zone = set()  # Track unique people IDs in alarm zone
        
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop video if it ends
            ret, frame = self.cap.read()

        self.frame_count += 1

        # --- AI PROCESSING ---
        if self.frame_count % 2 == 0:  # Reduced from 3 to 2 for better tracking consistency
            current_conf = self.conf_var.get() / 100.0 
            
            # 1. Run YOLO with optimized parameters
            results = self.model(frame, conf=current_conf, imgsz=YOLO_IMG_SIZE, iou=YOLO_NMS_CONF)[0]
            detections = sv.Detections.from_ultralytics(results)
            detections = detections[detections.class_id == 0]
            
            # 2a. FILTER: Remove tiny detections (likely false positives)
            if len(detections) > 0:
                widths = detections.xyxy[:, 2] - detections.xyxy[:, 0]
                heights = detections.xyxy[:, 3] - detections.xyxy[:, 1]
                min_size = 20  # Minimum bounding box width/height in pixels
                valid_size = (widths >= min_size) & (heights >= min_size)
                detections = detections[valid_size]
            
            # 2b. FILTER: Blue Exclusion Zones (KILL THE POLES FIRST)
            if self.exclusion_zones and len(detections) > 0:
                widths = detections.xyxy[:, 2] - detections.xyxy[:, 0]
                heights = detections.xyxy[:, 3] - detections.xyxy[:, 1]
                aspect_ratios = heights / widths
                keep_mask = np.ones(len(detections), dtype=bool)
                
                for excl_zone in self.exclusion_zones:
                    in_this_zone = excl_zone.trigger(detections=detections)
                    for i in range(len(detections)):
                        # Filter out pole-like detections in exclusion zones (tall and narrow)
                        if in_this_zone[i] and aspect_ratios[i] > 2.5:
                            keep_mask[i] = False
                            
                detections = detections[keep_mask]

            # 3. TRACKING: Assign IDs to the surviving humans
            detections = self.tracker.update_with_detections(detections)
            
            # 4. COUNTING: Track unique people who entered the alarm zone
            is_inside = self.zone.trigger(detections=detections)
            for idx, inside in enumerate(is_inside):
                # Ensure the detection has an ID before adding it to the set
                if inside and detections.tracker_id is not None:
                    self.unique_people_in_zone.add(int(detections.tracker_id[idx]))
            
            # Update the count label
            self.count_label.config(text=f"Total People: {len(self.unique_people_in_zone)}")
            
            self.last_detections = detections

        # --- DRAWING ---
        if self.last_detections is not None:
            is_inside = self.zone.trigger(detections=self.last_detections)
            if is_inside.any():
                cv2.putText(frame, "ALERT: ZONE BREACH", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            
            # Generate labels showing tracking ID and Confidence (e.g., "#5 88%")
            labels = []
            for i in range(len(self.last_detections)):
                tracker_id = self.last_detections.tracker_id[i] if self.last_detections.tracker_id is not None else "N/A"
                conf = int(self.last_detections.confidence[i] * 100)
                labels.append(f"#{tracker_id} {conf}%")
            
            # Draw Paths, Boxes, and Labels
            frame = self.trace_annotator.annotate(scene=frame, detections=self.last_detections)
            frame = self.box_annotator.annotate(scene=frame, detections=self.last_detections)
            frame = self.label_annotator.annotate(scene=frame, detections=self.last_detections, labels=labels)
            
        frame = self.zone_annotator.annotate(scene=frame)
        for annotator in self.excl_annotators:
            frame = annotator.annotate(scene=frame)

        # --- TKINTER IMAGE CONVERSION ---
        frame_resized = cv2.resize(frame, (960, 540))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        self.current_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        
        self.video_canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)

        # --- LOOP TRIGGER ---
        self.root.after(15, self.update_frame)

    def quit_app(self):
        self.cap.release()
        self.root.destroy()

# ==========================================
# LAUNCH THE APP
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SecurityDashboard(root)
    root.mainloop()
