from image_processing.augmented_reality import run_ar_pipeline_for_single_img
from image_processing.object_detection import detect_object
from flask_app.run import app as flask_app

import os
import fire


def main(part: int, img_path: str = "") -> None:
    """
    Main entry point for the command-line interface.

    Args:
        Part (int): Specify `1` for Part 1 or `3` for Part 3
        img_path (str): The file path to the input image.
    Example:
        >>> python3 src\main.py 3 assets\data\shelf-2635275_1280.jpg
    """
    if part == 1:
        print("--- Running Part 1: Object Detection ---")
        output = detect_object(img_path)
        print("Detection output:", output)
    elif part == 2:
        print("--- Running Part 2: Backend API ---")
        flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), threaded=True)
    elif part == 3:
        print("--- Running Part 3: AR Pipeline ---")
        run_ar_pipeline_for_single_img(img_path)
    else:
        raise Exception("Invalid part. Please specify `1` for Part 1 or `3` for Part 3")


if __name__ == '__main__':
    fire.Fire(main)