# Boundary Detection System

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/your-username/boundary_detection?style=flat-square)](https://github.com/your-username/boundary_detection/stargazers)

An AI-powered object detection and boundary monitoring system using YOLOv8 and Python. This project enables real-time detection of persons/objects crossing into defined alarm zones with visual alerts and optional GUI dashboard.

**[📖 Full Documentation](#documentation) | [🚀 Quick Start](#quick-start) | [🤝 Contributing](CONTRIBUTING.md) | [📦 Dataset](https://roboflow.com)**

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
   git clone https://github.com/your-username/boundary_detection.git
   cd boundary_detection
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download pre-trained models** (optional):
   - The `yolov8n.pt` model will be auto-downloaded on first run
   - For `upgraded_model.pt`, see [models/README.md](models/README.md)

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
- Verify the file path is correct (use absolute paths if relative paths fail)

### No Detections
- Reduce confidence threshold: `model(frame, conf=0.3)` 
- Check that the model path is correct
- Verify the video quality is sufficient for detection (clear, well-lit)
- Consider training a custom model on your specific use case (see [scripts/train.py](scripts/train.py))
- Try with `yolov8n.pt` if using custom model
- Check console output for error messages

### False Alarms
- Use exclusion zones to mask areas with false positives
- Adjust the polygon coordinates for your alarm zone
- Increase confidence threshold for stricter detection
- Check aspect ratio filtering in `boundary_alert3.py` and `boundary_alert4.py`

### Performance Issues
- Use the nano model (`yolov8n.pt`) for faster inference
- Reduce video resolution in the script
- Lower detection frequency (process every Nth frame with `if frame_count % 3 == 0`)
- Enable GPU acceleration (CUDA) if available
- Close other applications to free up system memory

### Installation Issues
```bash
# If pip install fails, try upgrading pip
pip install --upgrade pip

# For GPU support (CUDA), install torch separately
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify installation
python src/test.py
```

### Virtual Environment Issues
```bash
# Recreate venv if corrupted
rm -r venv  # or rmdir venv /s /q on Windows
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Getting Help

1. **Check the [FAQ](#troubleshooting) section above**
2. **Review [CONTRIBUTING.md](CONTRIBUTING.md) for issue templates**
3. **Search existing [GitHub Issues](https://github.com/your-username/boundary_detection/issues)**
4. **Create a new issue with:**
   - Clear description and screenshots
   - Full error message/traceback
   - Your system info (OS, Python version, GPU/CPU)

## Requirements

Key Python packages:
- `ultralytics` - YOLOv8 implementation
- `supervision` - Object detection utilities
- `opencv-python` - Video processing
- `pillow` - Image manipulation
- `numpy` - Numerical operations

## Future Enhancements

- [ ] Web-based dashboard (Flask/Django)
- [ ] Multi-camera support
- [ ] Persistent logging and alerting
- [ ] Email/SMS notifications
- [ ] Advanced analytics and statistics
- [ ] Support for additional model architectures
- [ ] REST API for third-party integrations
- [ ] Mobile app for monitoring
- [ ] Real-time cloud streaming

## Related Resources

- **Dataset**: [Download from Roboflow](https://roboflow.com) (original source)
- **YOLOv8 Docs**: [ultralytics.com](https://docs.ultralytics.com/)
- **Supervision**: [GitHub - roboflow/supervision](https://github.com/roboflow/supervision)
- **OpenCV**: [opencv.org](https://opencv.org/)

## License

Include appropriate license information if applicable.

## Support & Contributing

- 📖 See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- 🐛 Report bugs in [GitHub Issues](https://github.com/your-username/boundary_detection/issues)
- 💬 Discuss features in [GitHub Discussions](https://github.com/your-username/boundary_detection/discussions)

---

**Made with ❤️ for security and monitoring**
