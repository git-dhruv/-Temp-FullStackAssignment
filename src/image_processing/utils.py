"""
@brief
Utils File for Image Manipulation
@author: Dhruv Parikh
@date: 2024-11-03
"""

import imageio
import cv2
from typing import List, Tuple
from numpy import ndarray

def load_gif(filename: str)->List[ndarray]:
    """
    Load a GIF file and convert its frames to BGR format.

    Args:
        filename: The path to the GIF file.

    Returns:
        List: A list of frames in BGR format.
    """
    gif = imageio.mimread(filename)
    frames = []
    for frame in gif:
        if len(frame.shape) == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frames.append(frame)
    return frames

def overlay_images(background: ndarray, overlay: ndarray, position: Tuple[int, int] = (0, 0)) -> ndarray:
    """
    Overlays `overlay` onto `background` img at position
    @NOTE: Assumes the images have 3 channels. 
    
    Args:
        background: The background image.
        overlay: The overlay image to place on the background.
        position: The (x, y) coordinates where the overlay will be placed.
    Returns:
        ndarray: The combined image with the overlay applied to the background. 
    """
    assert (len(overlay.shape) == 3 and len(overlay.shape) == 3)

    x, y = position
    h, w, _ = overlay.shape
    if x + w > background.shape[1] or y + h > background.shape[0]:
        raise ValueError("Overlay image goes out of bounds.")
    background[y:y+h, x:x+w] = overlay
    return background