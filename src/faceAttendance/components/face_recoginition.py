import sqlite3
import face_recognition
import numpy as np
import cv2
import time
import ast
from pathlib import Path
from faceAttendance.utils.common import create_dirs
from faceAttendance.entity import FaceRecognitionConfig
from faceAttendance import logger

class FaceRecognition:
    def __init__(self, config: FaceRecognitionConfig):
        self.config = config

    def take_picture(self):
        create_dirs([self.config.root_dir])
        cap = cv2.VideoCapture(self.config.num_cam)

        if not cap.isOpened():
            logger.error("Error: Could not open webcam")
            return

        countdown_duration = self.config.countdown_seconds  # seconds
        countdown = countdown_duration
        countdown_active = False

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret:
                # Display the frame
                if countdown_active:
                    # Display countdown on the frame
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    countdown = countdown_duration - int(elapsed_time)

                    # Break if countdown is over
                    if countdown < 0:
                        cv2.imwrite(self.config.face_out_path, frame)
                        print("Last frame saved successfully as 'face.jpg'!")
                        break
                    cv2.putText(frame, str(countdown), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame, self.config.take_picture_msg, (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                cv2.imshow('Webcam', frame)

                # Check for key press
                key = cv2.waitKey(1)

                # Start countdown if 'p' is pressed
                if key == ord('p') and not countdown_active:
                    countdown_active = True
                    start_time = time.time()


                if key == ord('q'):
                    break

            else:
                logger.error("Error: Could not read frame from webcam")
                break
                
    def face_recognition(self):
        conn = sqlite3.connect(self.config.database)
        cursor = conn.cursor()
        target_image = face_recognition.load_image_file(self.config.face_out_path)
        cv2.imshow('face', target_image)
        cv2.waitKey(0)
        select_query = 'SELECT * FROM known_people'

        encoded_target = face_recognition.face_encodings(target_image)[0]
        
        if len(encoded_target) == 0:
            print("Error: Could not encode target image")
            return
        else:
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                row_encoded_list = ast.literal_eval(row[-1])
                row_encoded = np.array(row_encoded_list, dtype=np.float64)
                is_match = face_recognition.compare_faces([row_encoded], encoded_target)

                if is_match[0] == True:
                    logger.info(f"Match found for {row[2:-2]}")
                    break

            else:
                logger.info("No match found")

            conn.close()
            
                        
