from faceAttendance.config.configuration import ConfigurationManger
from faceAttendance.components.image_encoding import ImageEncoding
from faceAttendance import logger

STAGE_NAME = 'Image Encoding'

class ImageEncodingStagePipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManger()
        image_encoding_config = config.get_image_encoding_config()
        image_encoding = ImageEncoding(image_encoding_config)
        image_encoding.image_encoding()


if __name__ == "__main__":
    try: 
        logger.info(f'Starting {STAGE_NAME} stage')
        image_encoding_obj = ImageEncodingStagePipeline()
        image_encoding_obj.main()
        logger.info(f'Completed {STAGE_NAME} stage')
        
    except Exception as e:
        logger.exception(e)
        raise e
