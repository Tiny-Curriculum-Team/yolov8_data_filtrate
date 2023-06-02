from ultralytics import YOLO

# Load a model
model = YOLO("../../datasets/yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
metrics = model.val(data="../../datasets/mydata.yaml")  # train the model
metrics.box.map    # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps   # a list contains map50-95 of each category