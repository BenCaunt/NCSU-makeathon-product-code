import cv2
import json
import os
from datetime import datetime
from httpx import Response
from openai import OpenAI
import base64
from time import sleep,time


prompt = "You are a waste management system.  You are connected to two bins which are for recycling and trash, you will provide exclusively a json response with a label either TRASH or RECYCLE as well as a second description of what the item is.You will be given images, generally of a person holding the object and you will need to provide the above json response.  If you cannot decide what is in the image do not give up, worst case just say unknown and say the trash class. THE ONLY TWO VALID CLASSES ARE TRASH AND RECYCLE. Do not use the backtick formatting as this response is to be used algorithmically."

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def capture_and_save_image(cap):
    # Initialize the webcam
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Capture a single frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None

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
    encode_image_start = time()
    base64_image = encode_image(file_path)
    print(time() - encode_image_start)
    client = OpenAI(api_key = "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")

    # Replace 'model_id' with the appropriate model ID
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=50,
    )

    return json.loads(str(response.choices[0].message.content))

def capture_frame_and_assess(cap):
    image_path = capture_and_save_image(cap)
    if image_path:
        response = upload_to_api(image_path)
        type = response.get("label")
        print(type)
        return type
    return "TRASH"
def main():
    cap = cv2.VideoCapture(1)
    initial_time = time()
    # Capture and save image
    image_path = capture_and_save_image(cap)
    if image_path:
        # Upload to API and get response
        response = upload_to_api(image_path)
        print(response)
    print(time() - initial_time)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
