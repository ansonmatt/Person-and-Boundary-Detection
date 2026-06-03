# Boundary Detection System

An AI-powered object detection and boundary monitoring system using YOLOv8 and Python. This project enables real-time detection of persons/objects crossing into defined alarm zones with visual alerts and optional GUI dashboard.

## Features

- **Real-time Object Detection**: Uses YOLOv8 (nano and custom models) for fast, accurate object detection
- **Polygon-Based Zones**: Define custom alarm zones and exclusion zones as polygons
- **Multi-Zone Support**: Monitor multiple alarm zones simultaneously with different alert configurations
- **Object Tracking**: ByteTrack integration for tracking objects across frames with path tracing
- **Exclusion Zones**: Define blue exclusion zones to reduce false alarms from static objects
- **GUI Dashboard**: Interactive dashboard (`app.py`) with real-time video visualization and alerts
- **Video Processing**: Process pre-recorded videos or live camera feeds
- **Custom Model Training**: Train your own YOLOv8 models on custom datasets

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- OpenCV compatible system
- CUDA (optional, for GPU acceleration)

## Installation

1. **Clone or download the project**:
   ```bash
   cd boundary_detection
   ```

2. **Install dependencies**:
   ```bash
   pip install ultralytics supervision opencv-python pillow numpy
   ```

   For additional dependencies, check the imports in the Python files.

3. **Download pre-trained models** (optional):
   - `yolov8n.pt` - Nano model (lighter, faster)
   - `upgraded_model.pt` - Custom fine-tuned model (more accurate)

## Project Structure

```
boundary_detection/
├── src/                            # Application source code
│   ├── app.py                      # GUI Dashboard with interactive controls
│   ├── boundary_alert.py           # Simple boundary detection script
│   ├── boundary_alert2.py          # Alternative detection implementation
│   ├── boundary_alert3.py          # Another variation with tracking
│   ├── boundary_alert4.py          # Another variation with tracking
│   ├── get_coords.py               # Utility to extract zone coordinates
│   └── test.py                     # Testing and validation script
├── scripts/                        # Training and setup scripts
│   ├── train.py                    # Model training script
│   ├── download_dataset.py         # Dataset download utility
│   └── API Key                     # API credentials (keep private!)
├── datasets/                       # Training datasets
│   ├── data.yaml                   # Dataset configuration
│   ├── train/                      # Training images and labels
│   ├── valid/                      # Validation images and labels
│   └── test/                       # Test images and labels
├── models/                         # Model storage directory
├── upgraded_model.pt               # Custom trained YOLOv8 model
├── yolov8n.pt                      # Pre-trained YOLOv8 Nano model
├── runs/                           # Training outputs and logs
├── videos/                         # Input video files for processing
├── outputs/                        # Output directory for results
├── README.md                       # Project documentation
└── .gitignore                      # Git ignore rules (recommended)

```

## Quick Start

### Option 1: GUI Dashboard (Recommended)

1. **Configure the video and model** in `src/app.py`:
   ```python
   VIDEO_PATH = "videos/your_video.mp4"
   MODEL_PATH = "upgraded_model.pt"
   ```

2. **Define your alarm zone** by updating the `ALARM_POLYGON` coordinates:
   ```python
   ALARM_POLYGON = np.array([
       [x1, y1],  # Top-left
       [x2, y2],  # Top-right
       [x3, y3],  # Bottom-right
       [x4, y4]   # Bottom-left
   ])
   ```

3. **Run the dashboard**:
   ```bash
   python src/app.py
   ```

### Option 2: Simple Script

1. **Configure** `src/boundary_alert.py` with your video path and alarm zone coordinates
2. **Run**:
   ```bash
   python src/boundary_alert.py
   ```

## Configuration Guide

### Setting Alarm Zones

To define alarm zone coordinates:

1. Use `src/get_coords.py` to click on your video frame and extract pixel coordinates:
   ```bash
   python src/get_coords.py
   ```
   This will help you identify exact pixel positions for your polygon vertices.

2. Update the `ALARM_POLYGON` in your script with these coordinates:
   ```python
   ALARM_POLYGON = np.array([
       [900, 400],    # Top-left
       [1500, 400],   # Top-right
       [1500, 800],   # Bottom-right
       [900, 800]     # Bottom-left
   ])
   ```

### Setting Exclusion Zones (Optional)

Define blue exclusion zones to ignore false alarms in specific areas:

```python
EXCLUSION_ZONES_RAW = [
    np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]]),  # Zone 1
    np.array([[x5, y5], [x6, y6], [x7, y7], [x8, y8]]),  # Zone 2
]
```

## Models

### YOLOv8 Nano (`yolov8n.pt`)
- **Size**: ~6.3 MB
- **Speed**: Fast inference
- **Accuracy**: Good for general object detection
- **Best for**: Real-time monitoring with limited resources

### Upgraded Model (`upgraded_model.pt`)
- **Size**: Larger than nano
- **Speed**: Slightly slower but more accurate
- **Accuracy**: Fine-tuned on custom dataset
- **Best for**: Production use with higher accuracy requirements

## Training Custom Models

1. **Prepare your dataset**:
   - Organize images in `datasets/train/images` and `datasets/test/images`
   - Create corresponding label files in YOLO format
   - Create a `data.yaml` configuration file

2. **Configure training** in `scripts/train.py`:
   ```python
   model.train(
       data="datasets/data.yaml",
       epochs=50,
       imgsz=640,
       batch=8
   )
   ```

3. **Run training**:
   ```bash
   python scripts/train.py
   ```

4. **Use trained model** by updating `MODEL_PATH` in your scripts.

## File Descriptions

| File | Purpose |
|------|---------|
| `src/app.py` | Interactive GUI dashboard with real-time visualization |
| `src/boundary_alert.py` | Core boundary detection logic (simple version) |
| `src/boundary_alert2-4.py` | Alternative implementations or experimental versions |
| `src/get_coords.py` | Utility tool to extract pixel coordinates from video frames |
| `src/test.py` | Testing and validation script |
| `scripts/train.py` | YOLOv8 model training script |
| `scripts/download_dataset.py` | Automated dataset download utility |

## Troubleshooting

### Video Won't Load
- Check that `VIDEO_PATH` points to a valid video file
- Ensure the video codec is supported by OpenCV
- Try converting the video to a more common format (MP4, AVI)

### No Detections
- Reduce confidence threshold: `model(frame, conf=0.3)`
- Check that the model path is correct
- Verify the video quality is sufficient for detection
- Consider training a custom model on your specific use case

### False Alarms
- Use exclusion zones to mask areas with false positives
- Adjust the polygon coordinates for your alarm zone
- Increase confidence threshold for stricter detection

### Performance Issues
- Use the nano model (`yolov8n.pt`) for faster inference
- Reduce video resolution
- Lower detection frequency (process every Nth frame)
- Enable GPU acceleration (CUDA) if available

## Requirements

Key Python packages:
- `ultralytics` - YOLOv8 implementation
- `supervision` - Object detection utilities
- `opencv-python` - Video processing
- `pillow` - Image manipulation
- `numpy` - Numerical operations

## Future Enhancements

- [ ] Web-based dashboard
- [ ] Multi-camera support
- [ ] Persistent logging and alerting
- [ ] Email/SMS notifications
- [ ] Advanced analytics and statistics
- [ ] Support for additional model architectures

## License

Include appropriate license information if applicable.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the configuration guide
3. Ensure all dependencies are properly installed
4. Verify video and model files exist at specified paths
