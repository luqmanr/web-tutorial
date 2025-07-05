def inference_yolov8_model(model_path: str, image_path: str, conf_threshold: float = 0.25):
    """
    Performs inference on a single image using a specified YOLOv8 model.

    Args:
        model_path (str): Path to the trained or pre-trained YOLOv8 model weights (e.g., 'yolov8n.pt' or 'runs/detect/YOLOv8_COCO_Training/initial_run/weights/best.pt').
        image_path (str): Path to the image file for inference.
        conf_threshold (float): Confidence threshold for object detection. Detections below this will be filtered out.
    """
    print(f"\n--- Starting YOLOv8 Model Inference ---")
    print(f"Loading model from: {model_path}")
    print(f"Inference on image: {image_path}")

    # 1. Load the model for inference.
    try:
        model = YOLO(model_path)
        print(f"Successfully loaded model for inference: {model_path}")
    except Exception as e:
        print(f"Error loading model {model_path} for inference: {e}")
        print("Please ensure the model path is correct and the file exists.")
        return

    # 2. Check if the image file exists.
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'.")
        return

    # 3. Perform inference.
    # The 'predict' method returns a list of Results objects, one for each image.
    # 'save=True' will save the annotated image to 'runs/detect/predict/'.
    # 'conf' sets the confidence threshold for detections.
    # 'imgsz' ensures the input image is resized consistently.
    try:
        print("\n--- Running Prediction ---")
        results = model.predict(
            source=image_path,
            save=True,          # Save annotated images to 'runs/detect/predict'
            conf=conf_threshold,# Confidence threshold
            imgsz=IMAGE_SIZE    # Image size for inference
        )

        # Iterate through results (useful if source was a list of images or a folder)
        for i, r in enumerate(results):
            print(f"\n--- Results for image {i+1} ---")
            # Print detected objects and their confidence scores
            if r.boxes: # Check if any bounding boxes were detected
                print(f"Detected {len(r.boxes)} objects:")
                for box in r.boxes:
                    class_id = int(box.cls)
                    confidence = float(box.conf)
                    # Get class name from model's names attribute
                    class_name = model.names[class_id] if class_id in model.names else f"Class {class_id}"
                    print(f"  - Class: {class_name}, Confidence: {confidence:.2f}, BBox: {box.xyxy.tolist()[0]}")
            else:
                print("No objects detected.")

            # The path where the annotated image is saved
            save_dir = os.path.join(model.predictor.save_dir, os.path.basename(image_path))
            print(f"Annotated image saved to: {save_dir}")

        print("\n--- Inference Completed Successfully! ---")
    except Exception as e:
        print(f"An error occurred during inference: {e}")
        print("Please check the model path, image path, and Ultralytics installation.")

# Execute the training and/or inference functions when the script is run
if __name__ == "__main__":
    # --- Option 1: Train a new model and then perform inference ---
    # trained_model = train_yolov8_model()
    # if trained_model:
    #     # After training, the best model weights are typically saved in
    #     # 'runs/detect/PROJECT_NAME/RUN_NAME/weights/best.pt'
    #     # You'll need to update this path based on your PROJECT_NAME and RUN_NAME
    #     # Example: 'runs/detect/YOLOv8_COCO_Training/initial_run_with_augmentation/weights/best.pt'
    #     # Replace 'path/to/your/test_image.jpg' with an actual image path
    #     # inference_yolov8_model(
    #     #     model_path=f'runs/detect/{PROJECT_NAME}/{RUN_NAME}/weights/best.pt',
    #     #     image_path='path/to/your/test_image.jpg'
    #     # )
    #     pass # Placeholder if you don't want to run inference immediately after training

    # --- Option 2: Directly perform inference using a pre-trained or previously trained model ---
    # Replace 'path/to/your/image_for_inference.jpg' with the actual path to your image.
    # For a quick test, you can use a sample image from the internet or your local machine.
    # Example: You might download a sample image and place it in the same directory as this script.
    # Ensure the image file exists at the specified path.
    SAMPLE_IMAGE_PATH = 'cat.jpeg' # e.g., a photo of people, cars, etc.

    # You can use 'yolov8n.pt' for a quick test with a pre-trained model,
    # or specify the path to your own trained model weights (e.g., 'runs/detect/your_project/your_run/weights/best.pt')
    MODEL_FOR_INFERENCE = 'YOLOv8_COCO_Training/initial_run_with_augmentation3/weights/best.pt' # Or 'runs/detect/YOLOv8_COCO_Training/initial_run_with_augmentation/weights/best.pt'

    # Create a dummy image file for demonstration if it doesn't exist
    if not os.path.exists(SAMPLE_IMAGE_PATH):
        print(f"\n--- Creating a dummy image file for demonstration: {SAMPLE_IMAGE_PATH} ---")
        print("Please replace this with a real image for actual inference.")
        try:
            from PIL import Image, ImageDraw, ImageFont
            img = Image.new('RGB', (640, 480), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            try:
                # Try to load a default font
                fnt = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                # Fallback if arial.ttf is not found (common on some systems)
                fnt = ImageFont.load_default()
            d.text((10,10), "Hello YOLO!", fill=(255,255,0), font=fnt)
            d.text((10,60), "Place your image here", fill=(255,255,255), font=fnt)
            img.save(SAMPLE_IMAGE_PATH)
            print(f"Dummy image '{SAMPLE_IMAGE_PATH}' created.")
        except ImportError:
            print("Pillow library not found. Cannot create dummy image.")
            print("Please install Pillow: pip install Pillow")
            print(f"Or manually place a '{SAMPLE_IMAGE_PATH}' file in the script directory.")
        except Exception as e:
            print(f"Could not create dummy image: {e}")


    inference_yolov8_model(
        model_path=MODEL_FOR_INFERENCE,
        image_path=SAMPLE_IMAGE_PATH,
        conf_threshold=0.25 # Adjust confidence threshold as needed
    )
