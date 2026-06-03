import cv2
import numpy as np

# Load your test video
video_path = "videos/test3.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video {video_path}")
    exit()

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Video: {frame_width}x{frame_height} @ {fps} FPS ({total_frames} frames)")

# Scale down to fit on screen (max 1000x800)
max_display_width = 1000
max_display_height = 800
scale = min(max_display_width / frame_width, max_display_height / frame_height, 1.0)
display_width = int(frame_width * scale)
display_height = int(frame_height * scale)

print(f"Display size: {display_width}x{display_height} (scale: {scale:.2f})")

# Coordinate scaling factor (to convert display coords back to original)
coord_scale = 1.0 / scale

# State tracking
frame_idx = 0
ret, current_frame = cap.read()
display_frame = current_frame.copy()
collected_points = []
mouse_x, mouse_y = 0, 0

def click_event(event, x, y, flags, params):
    """Handle mouse clicks to collect coordinates"""
    global collected_points, display_frame, current_frame
    
    # Track mouse position for crosshair
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Scale coordinates back to original frame size
        orig_x = int(x * coord_scale)
        orig_y = int(y * coord_scale)
        
        # Add point to collection
        collected_points.append([orig_x, orig_y])
        print(f"✓ Point {len(collected_points)}: [{orig_x}, {orig_y}]")
        
        # Draw circle at click location
        cv2.circle(display_frame, (x, y), 8, (0, 255, 0), -1)
        cv2.circle(display_frame, (x, y), 10, (0, 255, 0), 2)
        
        # Draw polygon if we have 2+ points
        if len(collected_points) > 1:
            scaled_pts = np.array([(int(pt[0]*scale), int(pt[1]*scale)) for pt in collected_points], dtype=np.int32)
            cv2.polylines(display_frame, [scaled_pts], False, (0, 255, 0), 2)
        
        cv2.imshow("Full Image Coordinate Picker", display_frame)
    
    elif event == cv2.EVENT_MOUSEMOVE:
        # Scale to original coordinates for display
        orig_x = int(x * coord_scale)
        orig_y = int(y * coord_scale)
        
        # Draw crosshair on mouse move for live preview
        temp_frame = cv2.resize(current_frame, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
        
        # Draw all collected points (scaled)
        for i, pt in enumerate(collected_points):
            scaled_pt = (int(pt[0]*scale), int(pt[1]*scale))
            cv2.circle(temp_frame, scaled_pt, 8, (0, 255, 0), -1)
            cv2.putText(temp_frame, str(i+1), (scaled_pt[0]+12, scaled_pt[1]+5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw polygon if we have 2+ points
        if len(collected_points) > 1:
            scaled_pts = np.array([(int(pt[0]*scale), int(pt[1]*scale)) for pt in collected_points], dtype=np.int32)
            cv2.polylines(temp_frame, [scaled_pts], False, (0, 255, 0), 2)
        
        # Draw crosshair at current mouse position
        cv2.line(temp_frame, (x, 0), (x, display_height), (255, 0, 0), 1)  # Vertical
        cv2.line(temp_frame, (0, y), (display_width, y), (255, 0, 0), 1)    # Horizontal
        cv2.circle(temp_frame, (x, y), 5, (255, 0, 0), -1)                 # Center dot
        
        # Display coordinates at top-left (show original frame coords)
        coord_text = f"Original: [{orig_x}, {orig_y}] | Display: [{x}, {y}]"
        cv2.putText(temp_frame, coord_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        # Display collected points count
        points_text = f"Points collected: {len(collected_points)}"
        cv2.putText(temp_frame, points_text, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display frame info
        frame_text = f"Frame: {frame_idx+1}/{total_frames}"
        cv2.putText(temp_frame, frame_text, (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        cv2.imshow("Full Image Coordinate Picker", temp_frame)

def update_display():
    """Update the display frame with annotations"""
    global display_frame, current_frame, collected_points
    
    # Resize frame to fit on screen
    display_frame = cv2.resize(current_frame, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
    
    # Draw all collected points (scaled to display size)
    for i, pt in enumerate(collected_points):
        scaled_pt = (int(pt[0]*scale), int(pt[1]*scale))
        cv2.circle(display_frame, scaled_pt, 8, (0, 255, 0), -1)
        cv2.putText(display_frame, str(i+1), (scaled_pt[0]+12, scaled_pt[1]+5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Draw polygon if we have 2+ points
    if len(collected_points) > 1:
        scaled_pts = np.array([(int(pt[0]*scale), int(pt[1]*scale)) for pt in collected_points], dtype=np.int32)
        cv2.polylines(display_frame, [scaled_pts], False, (0, 255, 0), 2)
    
    # Display info text
    info_text = [
        f"Points: {len(collected_points)} | Frame: {frame_idx+1}/{total_frames} | Scale: {scale:.2f}",
        "CLICK to add point | 'n/→' next | 'p/←' prev | 'r' reset | 'c' copy | 'q' quit"
    ]
    
    for i, text in enumerate(info_text):
        cv2.putText(display_frame, text, (10, 30 + i*30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    cv2.imshow("Full Image Coordinate Picker", display_frame)

if ret:
    print("\n" + "="*60)
    print("FULL IMAGE COORDINATE PICKER")
    print("="*60)
    print("INSTRUCTIONS:")
    print("  • CLICK corners to collect coordinates")
    print("  • MOVE MOUSE to see crosshair and live coordinates")
    print("  • 'n' or '→' : Next frame")
    print("  • 'p' or '←' : Previous frame")
    print("  • 'r'        : Reset all points")
    print("  • 'c'        : Copy points as list")
    print("  • 'q'        : Quit")
    print("="*60 + "\n")
    
    cv2.namedWindow("Full Image Coordinate Picker")
    cv2.setMouseCallback("Full Image Coordinate Picker", click_event)
    
    update_display()
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        
        elif key == ord('n') or key == 83:  # 'n' or right arrow
            # Next frame
            if frame_idx < total_frames - 1:
                frame_idx += 1
                ret, current_frame = cap.read()
                update_display()
                print(f"→ Frame: {frame_idx+1}/{total_frames}")
        
        elif key == ord('p') or key == 81:  # 'p' or left arrow
            # Previous frame
            if frame_idx > 0:
                frame_idx -= 1
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, current_frame = cap.read()
                update_display()
                print(f"← Frame: {frame_idx+1}/{total_frames}")
        
        elif key == ord('r'):
            # Reset points
            collected_points = []
            update_display()
            print("🔄 Reset: All points cleared")
        
        elif key == ord('c'):
            # Copy points as Python list
            if collected_points:
                print("\n📋 Copy this polygon:")
                print("ALARM_POLYGON = np.array([")
                for pt in collected_points:
                    print(f"    {pt},")
                print("])")
                print()
        
        elif key == ord(' '):
            # Space to play/pause through frames
            while True:
                sub_key = cv2.waitKey(int(1000/fps)) & 0xFF
                if sub_key == ord(' '):
                    break
                elif sub_key == ord('q'):
                    break
                frame_idx += 1
                if frame_idx >= total_frames:
                    frame_idx = 0
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                else:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, current_frame = cap.read()
                if not ret:
                    break
                update_display()

cap.release()
cv2.destroyAllWindows()

# Final summary
print("\n" + "="*60)
if collected_points:
    print("FINAL POLYGON:")
    print("ALARM_POLYGON = np.array([")
    for pt in collected_points:
        print(f"    {pt},")
    print("])")
else:
    print("No points collected.")
print("="*60)
