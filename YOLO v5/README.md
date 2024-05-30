# Yolo v5


Steps For Training Custom YOLOv5 Object Detector With Custom Dataset
- Environmental set up and Installation of YOLOv5 dependencies
- Preprocessing Custom Dataset
- Define YOLOv5 Model Configuration and Architecture
- Train a custom YOLOv5 Detector
- Evaluate YOLOv5 performance
- Visualize YOLOv5 training data
- Run YOLOv5 Inference on test images
- Export Saved YOLOv5 Weights for Future Inference


### Environmental set up and Installation of YOLOv5 dependencies

```
$ git clone https://github.com/ultralytics/yolov5 # clone repo

$ pip install -U -r yolov5/requirements.txt # install dependencies

$ cd /content/yolov5 #change directory into project folder.
```



Image Label for YOLOv5 was made using LabelImg 

Steps: 
1. Install LabelImg 
```
pip install labelimg
```
2. Open an image using LabelImg
```
labelimg <path-to-the-image> <path-to-class.txt-file>
```
In the classes.txt file you need to list all the classes in new line. 
for example: 

```
car 
bike
truck 
```

