import sqlite3
import face_recognition
import numpy as np
import cv2
import json
from faceAttendance.entity import ImageEncodingConfig
from faceAttendance import logger


class ImageEncoding:
    def __init__(self, config: ImageEncodingConfig):
        self.config = config

    def image_encoding(self):
        conn = sqlite3.connect(self.config.database)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE known_people ADD COLUMN face_encoded TEXT")
        cursor.execute("SELECT id, image FROM known_people")
        rows = cursor.fetchall()

        for row in rows:
            image_id, image = row

            nparr = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            face_encoded = face_recognition.face_encodings(image)
            encoded_faces_list = [face.tolist() for face in face_encoded]
            encoded_face_json = json.dumps(encoded_faces_list)

            cursor.execute("UPDATE known_people SET face_encoded = ? WHERE id=?", (encoded_face_json, image_id))

        conn.commit()
        conn.close()

        logger.info(f'Image encoding completed')
    
