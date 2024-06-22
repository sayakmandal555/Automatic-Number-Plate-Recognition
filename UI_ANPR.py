import re
import cv2
import string
import easyocr
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import pandas as pd
import streamlit as st

# Initialize the OCR reader and YOLO models
reader = easyocr.Reader(['en'], gpu=True)
coco_model = YOLO("yolov8n.pt")
model = YOLO("license_plate_detector.pt")

# Define character mappings
int_to_char = {'0': 'O', '1': 'I', '2': 'Z', '3': 'B', '4': 'A', '5': 'S', '6': 'b', '7': 'T', '8': 'B', '9': 'q'}
char_to_int = {'A': '4', 'B': '8', 'b': '6', 'D': '0', 'G': '6', 'g': '9', 'I': '1', 'J': '7', 'L': '4', 'l': '1', 'O': '0', 'o': '0', 'q': '9', 'S': '5', 's': '5', 'T': '7', 'Z': '2', 'z': '2'}

# Function to perform OCR on an image
def perform_ocr(frame):
    ocr = reader.readtext(frame)
    return ocr

# Function to check license plate format
def license_complies_format(text):
    if len(text) == 10:
        if all(char in string.ascii_uppercase + ''.join(int_to_char.keys()) if i < 2 else char in '0123456789' + ''.join(char_to_int.keys()) for i, char in enumerate(text)):
            return True
    elif len(text) in [8, 9]:
        if all(char in string.ascii_uppercase + ''.join(int_to_char.keys()) if i < 2 else char in '0123456789' + ''.join(char_to_int.keys()) for i, char in enumerate(text)):
            return True
    return False

# Function to reformat license plate into expected correct format
def format_license(text):
    mapping = {0: int_to_char, 1: int_to_char, 4: int_to_char, 5: int_to_char,
               2: char_to_int, 3: char_to_int, 6: char_to_int, 7: char_to_int, 8: char_to_int, 9: char_to_int}
    license_plate_ = ''.join(mapping.get(i, {}).get(char, char) for i, char in enumerate(text))
    return license_plate_

# Streamlit UI components
st.title("Real-time License Plate Recognition")
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Save the uploaded file
    video_path = f"uploaded_video.{uploaded_file.name.split('.')[-1]}"
    with open(video_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    cap = cv2.VideoCapture(video_path)
    lp = ""
    frm_nm = -1
    ret = True

    stframe = st.empty()
    csv_output = []

    while ret:
        ret, frame = cap.read()
        frm_nm += 1

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detections = model(frame)[0]

            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                score = np.round(score, 2)

                if score >= 0.5:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    crop = frame[y1:y2, x1:x2]
                    dat = perform_ocr(crop)

                    for bbox, text, confidence in dat:
                        text = re.sub(r'[^a-zA-Z0-9]', '', text)
                        if len(text) >= 4 and len(text) <= 6:
                            p1 = text
                            lp += p1
                        elif len(text) in [8, 9, 10]:
                            lp = text

                        text = lp.upper()

                        if len(text) in [8, 9, 10] and license_complies_format(text):
                            formatted_text = format_license(text)
                            timestamp = datetime.now()
                            cv2.putText(frame, formatted_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                            csv_output.append([frm_nm, timestamp, formatted_text])

            stframe.image(frame, channels="RGB")
            if st.button('Stop Processing', key=frm_nm):
                break
        else:
            st.write("End of Frames!")
            break

    cap.release()
    df = pd.DataFrame(csv_output, columns=['Frame Number', 'Timestamp', 'License Plate Text'])
    df.drop_duplicates(subset=['License Plate Text'], inplace=True)

    # Save the result CSV
    result_csv = "result.csv"
    df.to_csv(result_csv, index=False)
    st.download_button("Download CSV", result_csv)
