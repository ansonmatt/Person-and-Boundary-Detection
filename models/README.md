# YOLOv8 Models

This folder contains references to the trained models used in the boundary detection system.

## Available Models

### `upgraded_model.pt` (Custom Fine-tuned)
- **Source**: Custom trained on boundary detection dataset
- **Size**: ~50MB
- **Accuracy**: High (optimized for your specific use case)
- **Download**: [Add link to your storage]

### `yolov8n.pt` (Pre-trained Nano)
- **Source**: Ultralytics YOLOv8 Nano
- **Size**: ~6.3MB
- **Accuracy**: Good for general purpose
- **Download**: Auto-downloaded by `ultralytics` library

## How to Download

### Automatic
```bash
# YOLOv8 models are automatically downloaded on first run
python src/app.py
```

### Manual
1. Download `upgraded_model.pt` from [your-storage-link]
2. Place it in the root directory: `boundary_detection/upgraded_model.pt`

## Model Specifications

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| yolov8n.pt | 6.3MB | Fast | Good | Real-time with limited resources |
| upgraded_model.pt | ~50MB | Medium | Excellent | Production with high accuracy |

## Training Your Own Model

See [scripts/train.py](../scripts/train.py) for training instructions.
