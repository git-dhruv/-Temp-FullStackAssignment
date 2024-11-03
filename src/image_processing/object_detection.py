"""
@brief
This module implements a simple object detection pipeline using Faster R-CNN model. 

@author: Dhruv Parikh
@date: 2024-11-03
"""

import torch
import numpy as np
import cv2
import json
import torchvision
from typing import Dict, List, Union

def detect_object(img_path : str = "") -> Dict[str, List[Union[str, np.ndarray]]]:
    """
    Detects objects in an image using a pre-trained Faster R-CNN model.

    Args: img_path: The file path to the input image.

    Returns: A dictionary containing:
        - 'labels': A list of detected object labels.
        - 'bbox': A list of bounding boxes for the detected objects, represented as numpy arrays.    

    Usage:
        >>> output = detect_object('path/to/your/image.jpg')
        >>> print("Detected labels:", output['labels'])
        >>> print("Bounding boxes:", output['bbox'])            
    """

    # Load Model
    faster_rcnn_model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights='FasterRCNN_ResNet50_FPN_Weights.DEFAULT', pretrained=True, box_score_thresh=0.7, box_nms_thresh=0.01)
    faster_rcnn_model.eval()
    category_names_from_coco_dataset = []
    with open(r'cfgs/category_names.json') as f:
        data = json.load(f)
        category_names_from_coco_dataset = data["COCO_INSTANCE_CATEGORY_NAMES"]
        valid_grocery_label = data["filtered_list"]

    # Image Preprocessing
    img_raw = cv2.imread(img_path)
    img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
    img_torch = torch.Tensor(img_raw).permute(2, 0, 1).unsqueeze(0).contiguous()
    img_torch = img_torch / 255.0

    # Inference
    raw_predictions = faster_rcnn_model(img_torch)[0]

    # Post Processing
    output = {'labels': [], 
              'bbox': []}
    for label, box in zip(raw_predictions['labels'], raw_predictions['boxes']):
       if category_names_from_coco_dataset[label] in valid_grocery_label:
           output['labels'].append(category_names_from_coco_dataset[label])
           output['bbox'].append(np.int32(box.detach().numpy()))
    return output