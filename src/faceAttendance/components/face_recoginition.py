import sqlite3
import face_recognition
import numpy as np
import cv2
import time
import ast
from pathlib import Path
from faceAttendance.utils.common import create_dirs
from faceAttendance.entity import FaceRecognitionConfig
import streamlit as st
from faceAttendance import logger

class FaceRecognition:
    def __init__(self, config: FaceRecognitionConfig, run_env: str='base'):
        self.config = config
        self.run_env = run_env
        self.FRAME_WINDOW = st.image([])

    def take_picture(self):
        create_dirs([self.config.root_dir])
        cap = cv2.VideoCapture(self.config.num_cam)

        if not cap.isOpened():
            logger.error("Error: Could not open webcam")
            return

        countdown_duration = self.config.countdown_seconds  # seconds
        countdown = countdown_duration
        countdown_active = False
        take_picture_button_clicked = st.button('Take Picture')
        stop_webcam = st.button('Stop webcam')
        key = None
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

                if self.run_env == 'base':
                    cv2.imshow('Webcam', frame)
                    # Check for key press
                    key = cv2.waitKey(1)

                # Start countdown if 'p' is pressed

                elif self.run_env == 'app':
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    key = cv2.waitKey(1)
                    self.FRAME_WINDOW.image(frame)

                if (key == ord('p') or take_picture_button_clicked) and not countdown_active:
                    countdown_active = True
                    start_time = time.time()

                if key == ord('q') or stop_webcam:
                    break

            else:
                logger.error("Error: Could not read frame from webcam")
                break
                
    def face_recognition(self):
        conn = sqlite3.connect(self.config.database)
        cursor = conn.cursor()
        target_image = face_recognition.load_image_file(self.config.face_out_path)
        target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
        if self.run_env == 'base':
            cv2.imshow('face', target_image)
            cv2.waitKey(0)
        # elif self.run_env == 'app':
        #     self.FRAME_WINDOW.image(target_image)

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
                    if self.run_env == 'app':
                        st.success(f"Match found for {row[2:-2]}")
                    else:
                        print(f"Match found for {row[2:-2]}")
                    
                    return


            else:
                if self.run_env == 'app':
                    st.warning("No match found")
                logger.info("No match found")

            conn.close()
            
                        
