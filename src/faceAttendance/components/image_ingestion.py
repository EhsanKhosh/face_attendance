from faceAttendance.entity import ImageIngestionConfig
from faceAttendance.utils.common import read_yaml
from faceAttendance import logger
from pathlib import Path
import sqlite3
import os

class ImageIngestion:
    def __init__(self, image_config:ImageIngestionConfig):
        self.config = image_config

    def create_database(self):
        conn = sqlite3.connect(os.path.join(self.config.database_path, 'FADatabase.db'))
        cursor = conn.cursor()
        create_table = '''
            CREATE TABLE IF NOT EXIST known_people (
                id INTEGER PRIMARY KEY,
                image BLOB,
                first_name TEXT,
                last_name TEXT,
                age INTEGER,
                gender TEXT,
                rating INTEGER,
        )
        '''
        cursor.execute(create_table)
        conn.commit()
        cursor.close()
        conn.close()

    def assign_data_to_persons(self):
        conn = sqlite3.connect(os.path.join(self.config.database_path, 'FADatabase.db'))
        cursor = conn.cursor()
        insert_query = '''
            INSERT INTO known_people (id, first_name, last_name, age, gender, rating) VALUES (?, ?, ?, ?, ?)
            '''

        people_data = read_yaml(self.config.known_people_data)
        for person in people_data['people']:
            cursor.execute(insert_query, (person['id'], person['first_name'], person['last_name'], person['age'], person['gender'], person['rating']))
        conn.commit()
        cursor.close()
        conn.close()

    def insert_images(self):
        conn = sqlite3.connect(os.path.join(self.config.database_path, 'FADatabase.db'))
        cursor = conn.cursor()
        image_dir = self.config.image_dir
        for filename in os.listdir(image_dir):
            # Extract first name and last name from filename
            first_name, last_name = filename.split('_')[0], filename.split('_')[1].split('.')[0]
            
            # Query the database to retrieve corresponding row
            query = '''
            SELECT * FROM known_people WHERE first_name=? AND last_name=?
            '''
            cursor.execute(query, (first_name, last_name))
            row = cursor.fetchone()
    
            # If a corresponding row is found, insert image data into the table
            if row:
                # Read image file as binary data
                with open(os.path.join(image_dir, filename), 'rb') as f:
                    image_data = f.read()
            
            # Insert image data into the known_people table
            update_sql = '''
            UPDATE known_people SET image=? WHERE first_name=? AND last_name=?
            '''
            cursor.execute(update_sql, (sqlite3.Binary(image_data), first_name, last_name))

        conn.commit()
        cursor.close()
        conn.close()


        