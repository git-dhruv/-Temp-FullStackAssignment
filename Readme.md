# Full Stack Developer Coding Test

## Setup:
### Create a venv (can be skipped)
- On Windows:
```bash python -m venv venv```
- Linux/MacOS
```python3 -m venv venv```
### Activate virtual env 

### Install Dependencies
`pip install -r requirements.txt`

## How to Run 
You can run different parts of the project using the following command format:
```python .\src\main.py PART IMG_PATH```

- Part 1: Object Detection
```python .\src\main.py 1 assets\data\shelf-2635275_1280.jpg```

- Part 2: Backend API
```python .\src\main.py 2```

- Part 3: AR
```python .\src\main.py 3 assets\data\shelf-2635275_1280.jpg```

## Assets
Images are located in `assets\data`. Configurations are located in `cfgs`


## About

The project implements object detection using FasterRCNN, processes the output and then overlays bounding box and labels on it. On top of this, a gif animation was added to increase scope. The aim was to keep the codebase simple and stateless while fulfilling the project requirements. For Part 2 please read `src\flask_app\Readme.md`. 

Note: This code was tested on Linux. There are problems parsing curl request using Powershell and I didn't investigated it further. 

### Design
- The project is split into 2 modules, augmented reality and object detection.

Object Detection works by using FasterRCNN from torch. This runs on CPU since its only detection and not tracking (which requires high speed). The following networks were investigated: 
- YOLOv5
- YOLONAS
- FasterRCNN (All verions offerred by torch)

Both YOLO networks were offered by ultralytics that had a complete api which worked well but meant all work will be done by the api. Hence that approach was discarded. FasterRCNN was another choice for Object Detection, which work okayish. This was expected since the networks are trained on COCO while the images are random and certainly OOD. The model normalizes images based on the COCO distribution, resulting in suboptimal performance on random images.


Fine-tuning on OOD images is an option, but it is beyond the scope of this evaluation. Other methods, such as template matching, are not robust against variations in scale and lighting. Additionally, pruning feature correspondences requires extensive tuning, whereas post-processing for neural network approaches involves straightforward non-maximum suppression (NMS) and confidence thresholds.

### What should be explored
The introduction of Vision Transformers initially resulted in lower performance compared to YOLO. However, subsequent variants like Swin Transformers and DeTR demonstrated improved performance with reduced data requirements. In my experience, object detection and segmentation benefit from global context for better accuracy, although this also increases data demands for training.
