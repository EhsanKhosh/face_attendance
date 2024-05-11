import streamlit as st
from PIL import Image
from faceAttendance.pipeline.stage_03_face_recognition import FaceRecognitionStagePipeline
import threading
import cv2
import numpy as np

# Function to handle button clicks and navigation
def handle_click(button_id):
    if button_id == 'webcam':
        st.session_state['page'] = 'webcam'
    elif button_id == 'upload':
        st.session_state['page'] = 'upload'

# Function to display content based on navigation
def show_page(page):
    if page == 'home':
        st.title('Welcome to Face Attendance')
        st.write("Choose an option below for face recognition.")
    elif page == 'webcam':
        st.title('Face Attendance by Webcam')
        st.write("Webcam feature is under development.")
        st.write("Please wait while the webcam initializes...")
        st.subheader("Webcam Live Feed")
        # Start face recognition using webcam
        face_recognition_pipeline = FaceRecognitionStagePipeline(run_env='app')
        face_recognition_pipeline.main()
        # Function to continuously update webcam feed

    elif page == 'upload':
        st.title('Face Recognition by Image')
        uploaded_file = st.file_uploader("Choose an image file")
        if uploaded_file is not None:
            st.write("Image uploaded successfully.")
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            if st.button('Save Image'):
                cv2.imwrite('/home/ehsan/PycharmProjects/Computer-Vision/face_attendance/artifacts/face_recognition/face.jpg',np.asarray(image))
            # Start face recognition using uploaded image
                face_recognition_pipeline = FaceRecognitionStagePipeline(run_env='app', take_picture=False)
                face_recognition_pipeline.main()
        else:
            st.write("No image uploaded.")

# Sidebar with buttons
st.sidebar.title('Face Attendance')
if st.sidebar.button('Use Webcam for Face Attendance', key='webcam'):
    handle_click('webcam')
if st.sidebar.button('Upload Image for Face Attendance', key='upload'):
    handle_click('upload')

# Check if the app is running with Streamlit
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'  # Set the default page

# Display content based on current page
show_page(st.session_state['page'])
