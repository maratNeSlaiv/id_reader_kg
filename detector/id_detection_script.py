from PIL import Image
import cv2
from ultralytics import YOLO
import numpy as np

def detect_id_cards(image : np.array, model, confidence_threshold=0.8):
    results = model(image)
    
    boxes = results[0].boxes.xyxy.tolist()
    confidences = results[0].boxes.conf.tolist()
    
    # Filter detections for ID cards with confidence > confidence_threshold
    id_card_detections = [(box, confidence) for box, confidence in zip(boxes, confidences) if confidence > confidence_threshold]

    if len(id_card_detections) == 0:
        # No ID cards detected or all detections have low confidence
        print('No id cards found. However we still gonna proceed.')
        return [image], 0
    
    cropped_images = []
    for box, confidence in id_card_detections:
        x1, y1, x2, y2 = [int(x) for x in box]
        print('box values:', x1, y1, x2, y2)
        
        cropped_image = image[y1:y2, x1:x2]
        cropped_images.append(cropped_image)

    return cropped_images, len(id_card_detections)

# Example usage
img_path = '/Users/maratorozaliev/Desktop/front_views/ID1657253.jpg'
model_path = '/Users/maratorozaliev/Desktop/id_reader/detector/ID_detection.pt'
model = YOLO(model_path)
image = cv2.imread(img_path)
id_cards, num_found = detect_id_cards(image, model)

if num_found > 0:
    print(f"Found {num_found} ID card(s).")
    # Process id_cards as needed
else:
    print("No ID cards found.")
