from faceAttendance.config.configuration import ConfigurationManger
from faceAttendance.components.image_ingestion import ImageIngestion
from faceAttendance import logger

STAGE_NAME = 'Image Ingestion'

class ImageIngestionStagePipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManger()
        image_ingestion_config = config.get_image_ingestion_config()
        image_ingestion = ImageIngestion(image_ingestion_config)
        image_ingestion.create_database()
        image_ingestion.assign_data_to_persons()
        image_ingestion.insert_images()


if __name__ == '__main__':
    try: 
        logger.info(f'Starting {STAGE_NAME} stage')
        image_ingestion_obj = ImageIngestionStagePipeline()
        image_ingestion_obj.main()
        logger.info(f'Completed {STAGE_NAME} stage')
        
    except Exception as e:
        logger.exception(e)
        raise e