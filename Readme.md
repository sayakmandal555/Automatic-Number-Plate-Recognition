![image](https://github.com/bittu5555/Automatic-Number-Plate-Recognition/assets/106305917/b575d928-9094-49d7-add8-6ac8f371abb9)

**Introduction**

This system based on automatically recognize license plates from videos. It captures video frames, find the license plate in each frame, recognize the text on the license plate, and check if the text is in correct format (e.g., the right number of characters). The system can then save this information to a csv file. The system uses two different YOLO models to find cars in the video and then to find license plates on the cars. It uses EasyOCR to read the text on the license plate. Finally, it checks the text to make sure it follows the correct format. This system is useful because it can automatically recognize license plates from videos.

**Library used**

* **OpenCV (cv2):** For video capture, frame processing, and display.
* **NumPy (np):** For numerical operations and array manipulation.
* **CSV:** For handling CSV file operations such as reading and writing.
* **String:** For string manipulation and character checks.
* **EasyOCR:** For Optical Character Recognition tasks.
* **Ultralytics YOLO:** For object detection using YOLO models.
* **Matplotlib (plt):** For visualization and plotting (optional).

**Work flow**

* **Import Libraries:** Import the necessary libraries.
  
* **Define Functions:**
•	real_time(): This function performs the core license plate detection and recognition tasks.
•	perform_ocr(frame): Takes a frame (image) as input and performs OCR using EasyOCR to extract text from the detected license plate.
•	write_csv(csv_writer, frm_nm, time, text): Writes the frame number, timestamp, and recognized license plate text to a CSV file.
•	license_complies_format(text): Checks if the length and format of the recognized text match the expected license plate format (India in this case).
•	format_license(text): Reformats the recognized text based on a mapping between detected characters and their potential misreadings (due to similar shapes).

* **Real-time Processing (real_time() function):**
  
	* Initializes a reader for EasyOCR.

	* Loads two YOLO models: 
	* coco_model: for object detection (detecting vehicles).
	* model: specifically trained to detect license plates.
	* Defines a list vehicles containing class IDs for vehicles of interest (e.g., cars, motorcycles).

	* Opens a video capture object (cap) to read the video file specified in the path.

* **Loop through Video Frames:**
  
	* Reads a frame (frame) from the video capture.

	* Converts the frame from BGR (OpenCV color format) to RGB (EasyOCR format).

	* Uses coco_model to detect objects in the frame.

	* Iterates through detected objects (detections): 

	* Extracts information like bounding box coordinates (x1, y1, x2, y2), confidence score (score), and class ID (class_id).
	* If the confidence score is greater than or equal to 0.5 (indicating a likely detection): 
		* Draws a rectangle around the detected object (assumed license plate) on the frame.
		* Crops the frame based on the bounding box coordinates to isolate the license plate region.
		* Calls perform_ocr to extract text from the cropped image.
		* Iterates through recognized text (dat): 
		* Filters out detections with special characters or blank spaces using regular expressions.
		* Checks the length of the recognized text to match the expected license plate format (8 to 10 characters for India).
		* If the length matches a valid format: 
			* Calls license_complies_format to verify the text adheres to the specific format (e.g., two alphabets followed by four numbers).
			* If the format is valid, calls format_license to remap any potential misreadings.
			* Displays the formatted license plate text and bounding box on the frame.
			* Writes the frame number, timestamp, and formatted license plate text to the CSV file using write_csv.
* **Display and Save Results:**
	* Displays the processed frame with detections and license plate information using OpenCV.
	* Waits for a 'q' key press to quit the loop.
 * 
* **Post-processing (after exiting the loop):**
	* Reads the CSV file containing recognized license plates.
	* Uses Pandas to remove duplicate entries (based on license plate text) and saves the cleaned data to a new CSV file.

**Result:**

"P:\out.mp4"

