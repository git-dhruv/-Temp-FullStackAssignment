"""
@brief
This module implements an augmented reality pipeline that processes an image to detect objects 
and overlay animations based on detection results. It utilizes object detection and image manipulation 
techniques to create an engaging visual representation of detected objects.

@author: Dhruv Parikh
@date: 2024-11-03
"""

from image_processing.object_detection import detect_object
from image_processing.utils import load_gif, overlay_images, deepcopy_first_input

import cv2
import numpy as np

from copy import deepcopy
import warnings
from typing import Any, List

@deepcopy_first_input
def bounding_box_animation(raw_img : np.ndarray, frame_num : int, detections : List[int], max_frames_length: int) -> np.ndarray:
    """
    Render a frame by drawing a scaled bounding box based on the progression of the animation.

    Args:
        raw_img: The image to render on.
        frame_num: The current frame number in the animation.
        detections: The coordinates of the bounding box (x1, y1, x2, y2).
        max_frames_length: The total number of frames in the animation.

    Returns:
        The modified image with the bounding box drawn.
    """
    # % of how much we have progressed in animation
    frame_progression = np.clip(frame_num/max_frames_length, 0, 1)

    # Find Centroid and (height,width)
    x1, y1, x2, y2 = detections
    centroid_x = (x1 + x2) / 2
    centroid_y = (y1 + y2) / 2
    original_width = x2 - x1
    original_height = y2 - y1

    # Scale Box according to `frame_progression`
    new_width = original_width * (0.5 + 0.5 * frame_progression) 
    new_height = original_height * (0.5 + 0.5 * frame_progression)

    # Make new box from modified height and width
    new_x1 = int(centroid_x - new_width / 2)
    new_y1 = int(centroid_y - new_height / 2)
    new_x2 = int(centroid_x + new_width / 2)
    new_y2 = int(centroid_y + new_height / 2)
    cv2.rectangle(raw_img, (new_x1, new_y1), (new_x2, new_y2), color=(0, 255, 0), thickness=1)
    return raw_img    



def run_ar_pipeline_for_single_img(img_path : str) -> None:
    """
    Entry Function for the Part 3 of AR pipeline

    Args: 
        img_path: Path to raw image
    """
    img_raw = cv2.imread(img_path)
    
    predictions = detect_object(img_path)

    if len(predictions['bbox']) == 0:
        warnings.warn("No Object Detected!", RuntimeWarning)

    # Scanning Gif
    _internal_loading_gif_frame = load_gif('assets/internal/scan.gif')

    MAX_FRAMES = 240
    for frame_id in range(MAX_FRAMES):
        animated_img = deepcopy(img_raw)
        
        # Scanning Gif animation
        if frame_id < len(_internal_loading_gif_frame):
            # This can be made better by removing magic numbers and making it derived
            overlay = cv2.resize(_internal_loading_gif_frame[frame_id], (100,100))
            animated_img = overlay_images(img_raw, overlay, position=(50, 50)) 

        # Looping over all predictions for bbox
        for i in range(len(predictions['bbox'])):
            bbox = predictions['bbox'][i]

            # Bounding Box Animation
            animated_img = bounding_box_animation(animated_img, frame_id, bbox, MAX_FRAMES)
            # Text Animation
            label = predictions['labels'][i]
            how_much_to_print = int(1  + len(label) * frame_id/MAX_FRAMES)
            cv2.putText(animated_img, label[:how_much_to_print], (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow("Detection", animated_img)
        key = cv2.waitKey(15)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
