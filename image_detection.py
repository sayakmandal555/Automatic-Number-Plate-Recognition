import cv2
from paddleocr import PaddleOCR
import csv

ocr = PaddleOCR(lang='en')  # need to run only once to download and load model into memory
video_path = r"C:\Users\SAYAK\Downloads\Idiots on Bengaluru.mp4"  # Replace with the path to your video file
output_video_path = 'output_video_with_ocr.mp4'

# Open the video file
video_capture = cv2.VideoCapture(video_path)

# Get the video properties
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
num_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

# Create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Write OCR results to CSV file
csv_file = 'ocr_resul.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Frame', 'Text', 'Confidence', 'Coordinates'])

    for frame_number in range(num_frames):
        success, frame = video_capture.read()
        if not success:
            break

        # Perform OCR on the current frame
        result = ocr.ocr(frame, cls=False)
        
        for res in result:
            for line in res:
                text = line[1][0]
                confidence = line[1][1]
                coordinates = line[0]
                csv_writer.writerow([frame_number, text, confidence, coordinates])

        # Draw OCR results on the frame
        for res in result:
            for line in res:
                coordinates = line[0]
                cv2.putText(frame, line[1][0], (coordinates[0][0], coordinates[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Write the modified frame to the output video
        video_writer.write(frame)

# Release video objects
video_capture.release()
video_writer.release()

print("OCR results saved to", csv_file)
print("Video with OCR saved to", output_video_path)




'''from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(lang='en') # need to run only once to download and load model into memory
img_path = r"C:\Users\SAYAK\Downloads\mh.jpeg"
result = ocr.ocr(img_path, cls=False)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path="D:\AILABS_6 month\BakbakOne-Regular.ttf")
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')'''


'''from paddleocr import PaddleOCR
import csv

ocr = PaddleOCR(lang='en')  # need to run only once to download and load model into memory
img_path = r"C:\Users\SAYAK\Downloads\Indian_Vehicle_Registration_Plate_-_Kolkata_2011-07-29_4088.JPG"
result = ocr.ocr(img_path, cls=False)

# Write OCR results to CSV file
csv_file = 'ocr_result.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Text', 'Confidence', 'Coordinates'])

    for res in result:
        for line in res:
            text = line[1][0]
            confidence = line[1][1]
            coordinates = line[0]
            csv_writer.writerow([text, confidence, coordinates])

print("OCR results saved to", csv_file)
'''