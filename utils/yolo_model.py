from ultralytics import YOLO

def load_model():
    return YOLO("yolov8n.pt")  # or yolov5s.pt if preferred
