from faceAttendance.config.configuration import ConfigurationManger
from faceAttendance.components.face_recoginition import FaceRecognition
from faceAttendance import logger

STAGE_NAME = 'Face Recognition'

class FaceRecognitionStagePipeline:
    def __init__(self, run_env:str='base', take_picture=True):
        self.run_env = run_env
        self.take_picture = take_picture
    def main(self):
        config = ConfigurationManger()
        face_recognition_config = config.get_face_recognition_config()
        self.face_recognition = FaceRecognition(face_recognition_config, self.run_env)
        if self.take_picture:
            self.face_recognition.take_picture()
        self.face_recognition.face_recognition()
        


if __name__ == "__main__":
    try: 
        logger.info(f'Starting {STAGE_NAME} stage')
        face_recognition_obj = FaceRecognitionStagePipeline()
        face_recognition_obj.main()
        logger.info(f'Completed {STAGE_NAME} stage')
        
    except Exception as e:
        logger.exception(e)
        raise e