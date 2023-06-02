from ultralytics import YOLO

# Load a model
model = YOLO('../../models/v8/yolov8n.yaml').load("../../datasets/yolov8n.pt")  # build from YAML and transfer weights

# Train the model
model.train(data='../../datasets/mydata.yaml', epochs=100, imgsz=640, device='1')
