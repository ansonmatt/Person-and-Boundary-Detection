from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(
    data="datasets/data.yaml",
    epochs=10,
    imgsz=224,
    batch=8
)

print("Training complete!")