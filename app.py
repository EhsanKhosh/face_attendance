import streamlit as st
from PIL import Image
from faceAttendance.pipeline.stage_03_face_recognition import FaceRecognitionStagePipeline
from faceAttendance.components.face_recoginition import FaceRecognition
from faceAttendance.config.configuration import ConfigurationManger
import cv2
import numpy as np
import os
import sqlite3
import json
import face_recognition

# Define the path for the previous image
previous_image_path = '/home/ehsan/PycharmProjects/Computer-Vision/face_attendance/artifacts/face_recognition/face.jpg'

# Function to handle button clicks and navigation
def handle_click(button_id):
    st.session_state['page'] = button_id

# Function to display content based on navigation
def show_page(page):
    image = None
    if page == 'home':
        st.title('Welcome to Face Attendance')
        st.write("Choose an option below for face recognition.")
        if os.path.exists(previous_image_path):
            os.remove(previous_image_path)
    elif page == 'webcam':
        st.title('Face Attendance by Webcam')
        st.write("Webcam feature is under development.")
        st.write("Please wait while the webcam initializes...")
        st.subheader("Webcam Live Feed")
        # Start face recognition using webcam
        face_recognition_pipeline = FaceRecognitionStagePipeline(run_env='app')
        face_recognition_pipeline.main()
    elif page == 'upload':
        st.title('Face Recognition by Image')
        uploaded_file = st.file_uploader("Choose an image file")
        if uploaded_file is not None:
            st.write("Image uploaded successfully.")
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            if st.button('Save Image', key='save_image'):
                cv2.imwrite(previous_image_path, np.asarray(image))
                # Start face recognition using uploaded image
                face_recognition_pipeline = FaceRecognitionStagePipeline(run_env='app', take_picture=False)
                face_recognition_pipeline.main()
        else:
            st.write("No image uploaded.")
    elif page == 'register':
        st.title('Register New Face')

        st.write('Please enter your registration information')
        image_provider = st.radio('Choose option for importing face image', ('Webcam', 'Upload'))
            
        if image_provider == 'Upload':
            config = ConfigurationManger().get_face_recognition_config()
            face_recognition_obj = FaceRecognition(config=config, run_env='app')
            if os.path.exists(previous_image_path):
                
                previous_image = cv2.imread(previous_image_path)
                st.image(previous_image, caption='Previous image that you uploaded.', use_column_width=True)
                use_prev_image = st.checkbox('Use Previous Image', value=True)

                if use_prev_image:
                    image = cv2.imread(previous_image_path)
                else:
                    uploaded_file = st.file_uploader("Upload your face image", key="upload_new_image")
                    if uploaded_file is not None:
                        st.write("Image uploaded successfully.")
                        image_data = uploaded_file.read()
                        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        st.image(image, caption='Uploaded Image.', use_column_width=True)
                        cv2.imwrite(previous_image_path, np.asarray(image))
            else:
                uploaded_file = st.file_uploader("Upload your face image", key="upload_image")
                if uploaded_file is not None:
                    st.write("Image uploaded successfully.")
                    image_data = uploaded_file.read()
                    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                    st.image(image, caption='Uploaded Image.', use_column_width=True)
                    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
                    cv2.imwrite(previous_image_path, image)
        elif image_provider == 'Webcam':
            config = ConfigurationManger().get_face_recognition_config()
            face_recognition_obj = FaceRecognition(config=config, run_env='app')
            if st.button('Capture Image', key='capture_image'):
                st.session_state['start_countdown'] = True
                captured_image = face_recognition_obj.take_picture()
                if captured_image is not None:
                    st.image(captured_image, caption='Captured Image.', use_column_width=True)
                else:
                    st.error('Captured image is not available')

        with st.form('user_registration_form'):
            first_name = st.text_input('First Name')
            last_name = st.text_input('Last Name')
            age = st.number_input('Age', min_value=1, max_value=120, step=1)
            gender = st.selectbox('Gender', ('Male', 'Female'))
            submit_button = st.form_submit_button('Register')
                
        if submit_button:
            image = cv2.imread(previous_image_path, cv2.COLOR_BGR2RGB)
            if image is not None:
                target_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(target_image)
                if face_encodings:
                    if not face_recognition_obj.face_recognition():
                        face_encoded = face_encodings[0]
                        encoded_faces_list = [face.tolist() for face in face_encoded]
                        encoded_face_json = json.dumps(encoded_faces_list)

                        conn = sqlite3.connect('/home/ehsan/PycharmProjects/Computer-Vision/face_attendance/artifacts/database/FADatabase.db')
                        cursor = conn.cursor()
                        insert_query = '''
                            INSERT INTO known_people (image, first_name, last_name, age, gender, face_encoded) VALUES (?, ?, ?, ?, ?, ?)
                        '''
                        _, image_encoded = cv2.imencode('.jpg', image)
                        image_bin = sqlite3.Binary(image_encoded)
                        cursor.execute(insert_query, (image_bin, first_name, last_name, age, gender, encoded_face_json))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.write("Registration completed successfully.")
                        st.write('First name: ' + first_name)
                        st.write('Last name: ' + last_name)
                        st.write('Age: ' + str(age))
                        st.write('Gender: ' + gender)
                        st.image(image, caption='Registered Image.', use_column_width=True)
                    else:
                        st.error("Your face is registered before.You can try face attendance options.")
                else:
                    st.error("No face detected in the image. Please upload a different image.")
            else:
                st.error("Please upload or capture an image to register.")

# Sidebar with buttons
st.sidebar.title('Face Attendance')
if st.sidebar.button('Home', key='home'):
    handle_click('home')
if st.sidebar.button('Use Webcam for Face Attendance', key='webcam'):
    handle_click('webcam')
if st.sidebar.button('Upload Image for Face Attendance', key='upload'):
    handle_click('upload')
if st.sidebar.button('Register for Face Attendance', key='register'):
    handle_click('register')

# Check if the app is running with Streamlit
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # Set the default page

# Display content based on current page
show_page(st.session_state['page'])