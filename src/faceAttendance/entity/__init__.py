from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageIngestionConfig:
    root_dir : str
    database_path : str
    image_dir : str
    known_people_data: str

@dataclass(frozen=True)
class ImageEncodingConfig:
    root_dir : str
    database: str
    image_dir : str

@dataclass(frozen=True)
class FaceRecognitionConfig:
    root_dir : str
    database: str
    num_cam: int
    face_out_path: str
    countdown_seconds: int
    take_picture_msg: str
