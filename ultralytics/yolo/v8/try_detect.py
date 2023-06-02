from ultralytics import YOLO
import os
import numpy as np

model = YOLO('../../models/v8/yolov8n.yaml').load("./models/best.pt")
path_foundation = r"../../datasets/mydata/css-data/test/person"
inputs = []
for root, _, img_name in os.walk(path_foundation):
    random_list = np.random.randint(low=0, high=len(img_name), size=4)
    for i in random_list:
        inputs.append(os.path.join(root, img_name[i]))
results = model(inputs)  # list of Results objects
total_person = 0
for n,result in enumerate(results):
    boxes = result.boxes  # Boxes object for bbox outputs
    total_person += list(boxes.cls).count(5.)
    print(f"image_{n} person : {list(boxes.cls).count(5.)}")
print(total_person)
