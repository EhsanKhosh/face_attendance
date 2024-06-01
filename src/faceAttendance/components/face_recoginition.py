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
        self.FRAME_WINDOW = st.image([]) if run_env == 'app' else None
        self.countdown_active = False
        self.start_time = None
        self.loop_break = False

    def _display_frame(self, frame, countdown=None):
        if countdown is not None:
            cv2.putText(frame, str(countdown), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, self.config.take_picture_msg, (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        if self.run_env == 'app':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.FRAME_WINDOW.image(frame)
        elif self.run_env == 'base':
            cv2.imshow('Webcam', frame)

    def _handle_countdown(self, frame):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        countdown = self.config.countdown_seconds - int(elapsed_time)

        if countdown < 0:
            cv2.imwrite(self.config.face_out_path, frame)
            logger.info("Image captured successfully!")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return False, frame, None, True
        
        return True, frame, countdown, False

    def take_picture(self):
        create_dirs([self.config.root_dir])
        cap = cv2.VideoCapture(self.config.num_cam)

        if not cap.isOpened():
            logger.error("Error: Could not open webcam")
            return None

        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Error: Could not read frame from webcam")
                break

            if self.countdown_active:
                self.countdown_active, frame, countdown, self.loop_break = self._handle_countdown(frame)
                self._display_frame(frame, countdown)
            else:
                self._display_frame(frame)

            if self.run_env == 'app':
                if st.session_state.get('start_countdown', False):
                    self.countdown_active = True
                    self.start_time = time.time()
                    st.session_state['start_countdown'] = False
                if st.session_state.get('stop_webcam', False):
                    break
                if self.loop_break:
                    return frame

            elif self.run_env == 'base':
                key = cv2.waitKey(1)
                if key == ord('p') and not self.countdown_active:
                    self.countdown_active = True
                    self.start_time = time.time()
                if key == ord('q'):
                    break

        cap.release()
        if self.run_env == 'base':
            cv2.destroyAllWindows()

        if self.countdown_active:
            return frame
        return None
    
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
                        st.image(row[1], caption='face that matches with your face')
                    else:
                        print(f"Match found for {row[2:-2]}")
                    
                    return True


            else:
                if self.run_env == 'app':
                    st.warning("No match found")
                    
                logger.info("No match found")
                conn.close()
                return False


            
            
                        
