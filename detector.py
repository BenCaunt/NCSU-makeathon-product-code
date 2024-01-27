import cv2
import requests
import json
import os
from datetime import datetime
from openai import OpenAI

def capture_and_save_image():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None
    cap.release()
    cv2.destroyAllWindows()

    # Create a data folder if it doesn't exist
    data_folder = 'data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Generate a unique filename
    filename = f"{data_folder}/image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def upload_to_api(file_path):
    # Open the image file in binary mode
    with open(file_path, 'rb') as file:
        image_data = file.read()

    client = OpenAI()

    # Replace 'model_id' with the appropriate model ID
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": file_path,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    return response.choices[0]

def main():
    # Capture and save image
    image_path = capture_and_save_image()
    if image_path:
        # Upload to API and get response
        response = upload_to_api(image_path)
        print(response)

if __name__ == "__main__":
    main()
