import os
import requests
from io import BytesIO
from PIL import ImageDraw, ImageFont

# Fetch values securely from environment variables
PREDICTION_KEY = os.getenv("PREDICTION_KEY")
ENDPOINT = os.getenv("ENDPOINT")
PROJECT_ID = os.getenv("PROJECT_ID")
PUBLISHED_NAME = os.getenv("PUBLISHED_NAME")

def get_prediction(image_data):
    headers = {
        "Prediction-Key": PREDICTION_KEY,
        "Content-Type": "application/octet-stream"
    }

    url = f"{ENDPOINT}/customvision/v3.0/Prediction/{PROJECT_ID}/detect/iterations/{PUBLISHED_NAME}/image"

    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()
    return response.json()

def draw_bounding_boxes(image, predictions, threshold=0.5):
    draw = ImageDraw.Draw(image)

    # Load a bigger font
    try:
        font = ImageFont.truetype("arial.ttf", size=16)
    except IOError:
        font = ImageFont.load_default()

    for pred in predictions['predictions']:
        if pred['probability'] >= threshold:
            bbox = pred['boundingBox']
            left = bbox['left'] * image.width
            top = bbox['top'] * image.height
            width = bbox['width'] * image.width
            height = bbox['height'] * image.height

            # Draw the bounding box
            box_color = "red"
            text_color = "white"
            text_background = "green"

            draw.rectangle([left, top, left + width, top + height], outline=box_color, width=3)

            # Prepare text
            text = f"{pred['tagName']} ({pred['probability']:.2f})"
            
            # Use textbbox instead of textsize
            text_bbox = draw.textbbox((left, top), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Draw rectangle behind the text
            text_background_box = [left, top - text_height - 4, left + text_width + 4, top]
            draw.rectangle(text_background_box, fill=text_background)

            # Draw text
            draw.text((left + 2, top - text_height - 2), text, fill=text_color, font=font)

    return image






