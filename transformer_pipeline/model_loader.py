import time
from ultralytics import RTDETR

print("Downloading and initializing RT-DETR Vision Transformer...")

# Load the Large RT-DETR transformer model
model = RTDETR("rtdetr-l.pt")

print("Model loaded into memory successfully. Testing 1 frame...")

start_time = time.time()
# Run a test prediction on a standard image
results = model.predict("https://ultralytics.com/images/bus.jpg", save=False, verbose=False)
end_time = time.time()

print(f"\n--- SYSTEM CHECK COMPLETE ---")
print(f"SUCCESS: Transformer Model Loaded.")
print(f"Detected {len(results[0].boxes)} objects using Global Self-Attention.")
print(f"Time taken for 1 image: {end_time - start_time:.2f} seconds")