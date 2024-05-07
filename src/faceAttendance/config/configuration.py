from faceAttendance.entity import ImageIngestionConfig
from faceAttendance.utils.common import create_dirs, read_yaml
from faceAttendance.constants import *
from pathlib import Path


class ConfigurationManger():
    def __init__(self,
                config_path = CONFIG_FILE_PATH,
                params_path = PARAMS_FILE_PATH):
        self.config = read_yaml(Path(config_path))
        self.params = read_yaml(Path(params_path))
 
        create_dirs([self.config.artifacts_root])

    def get_image_ingestion_config(self) -> ImageIngestionConfig:
        config = self.config.image_ingestion
        image_ingestion_config = ImageIngestionConfig(
            root_dir = config.root_dir,
            database_path = config.database_path,
            image_dir = config.image_dir,
            known_people_data = config.known_people_data
        )
        return image_ingestion_config
        