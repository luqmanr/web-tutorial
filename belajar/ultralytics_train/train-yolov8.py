# Import the YOLO model from the ultralytics library
from ultralytics import YOLO
import os

# --- Configuration ---
# Path to your COCO dataset YAML file.
# This file defines the paths to your training/validation images and labels,
# as well as the class names.
# Make sure this path is correct for your system.
DATA_YAML_PATH = 'coco8.yaml'

# Specify the pre-trained model to use.
# For YOLOv8, you can use 'yolov8n.pt' (nano), 'yolov8s.pt' (small),
# 'yolov8m.pt' (medium), 'yolov8l.pt' (large), or 'yolov8x.pt' (extra-large).
# Choose based on your computational resources and desired performance.
# If YOLOv11 becomes available, you would replace this with 'yolov11n.pt' or similar.
MODEL_NAME = 'yolov8n.pt'

# Number of training epochs. More epochs can lead to better performance
# but also increase training time and risk of overfitting.
NUM_EPOCHS = 5

# Image size for training. Images will be resized to this dimension.
# Common sizes are 640, 1280.
IMAGE_SIZE = 640

# Batch size. Number of images processed in one training step.
# Adjust based on your GPU memory. Smaller values use less memory.
BATCH_SIZE = 16

# Name of the project and run for organizing results.
# Results will be saved in 'runs/detect/project_name/run_name'.
PROJECT_NAME = 'YOLOv8_COCO_Training'
RUN_NAME = 'initial_run_with_augmentation'

# --- Script Logic ---
def train_yolov8_model():
    """
    Initializes a YOLOv8 model and starts the training process.
    Includes notes on built-in augmentation and preprocessing.
    """
    print(f"--- Starting YOLOv8 Model Training ---")
    print(f"Model: {MODEL_NAME}")
    print(f"Dataset YAML: {DATA_YAML_PATH}")
    print(f"Epochs: {NUM_EPOCHS}")
    print(f"Image Size: {IMAGE_SIZE}")
    print(f"Batch Size: {BATCH_SIZE}")
    print(f"Project/Run: {PROJECT_NAME}/{RUN_NAME}")

    # 1. Load a pre-trained YOLO model.
    # This will download the model weights if not already present.
    try:
        model = YOLO(MODEL_NAME)
        print(f"Successfully loaded model: {MODEL_NAME}")
    except Exception as e:
        print(f"Error loading model {MODEL_NAME}: {e}")
        print("Please ensure you have ultralytics installed and an active internet connection to download weights.")
        return

    # 2. Check if the data YAML file exists.
    if not os.path.exists(DATA_YAML_PATH):
        print(f"Error: Data YAML file not found at '{DATA_YAML_PATH}'.")
        print("Please create the 'coco.yaml' file with your dataset configuration.")
        return

    # 3. Train the model.
    # Ultralytics YOLO models automatically handle a wide range of data augmentation
    # and preprocessing steps internally during training.
    # These include:
    # - Resizing images to 'imgsz'
    # - Normalization (scaling pixel values to a 0-1 range)
    # - Random Horizontal Flip (fliplr)
    # - Random Vertical Flip (flipud)
    # - Random Rotation (degrees)
    # - Random Translation (translate)
    # - Random Scaling (scale)
    # - Random Shear (shear)
    # - Random Perspective Transform (perspective)
    # - HSV Augmentation (hsv_h, hsv_s, hsv_v for hue, saturation, value)
    # - Mosaic Augmentation (combining 4 images into one)
    # - MixUp Augmentation (blending two images and their labels)
    # - Copy-Paste Augmentation (copying objects from one image to another)

    # You can control the intensity or enable/disable some of these augmentations
    # by passing specific arguments to the .train() method.
    # Below are some common augmentation parameters you can adjust:
    try:
        print("\n--- Initiating Training with Augmentation ---")
        results = model.train(
            data=DATA_YAML_PATH,
            epochs=NUM_EPOCHS,
            imgsz=IMAGE_SIZE,
            batch=BATCH_SIZE,
            project=PROJECT_NAME,
            name=RUN_NAME,
            # --- Augmentation Parameters (uncomment and adjust as needed) ---
            # hsv_h=0.015,   # image HSV-Hue augmentation (fraction)
            # hsv_s=0.7,     # image HSV-Saturation augmentation (fraction)
            # hsv_v=0.4,     # image HSV-Value augmentation (fraction)
            # degrees=0.0,   # image rotation (degrees)
            # translate=0.1, # image translation (fraction)
            # scale=0.5,     # image scale (fraction)
            # shear=0.0,     # image shear (degrees)
            # perspective=0.0,# image perspective (fraction), range 0.0-0.001
            # flipud=0.0,    # image flip up-down (probability)
            # fliplr=0.5,    # image flip left-right (probability)
            # mosaic=1.0,    # enable mosaic augmentation (probability)
            # mixup=0.0,     # enable mixup augmentation (probability)
            # copy_paste=0.0 # enable copy-paste augmentation (probability)
            # --- End Augmentation Parameters ---
        )
        print("\n--- Training Completed Successfully! ---")
        print(f"Results saved to: runs/detect/{PROJECT_NAME}/{RUN_NAME}")
    except Exception as e:
        print(f"An error occurred during training: {e}")
        print("Please check your dataset paths, YAML configuration, and system resources.")

# Execute the training function when the script is run
if __name__ == "__main__":
    train_yolov8_model()
