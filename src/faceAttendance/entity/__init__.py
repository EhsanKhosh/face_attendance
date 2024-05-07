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
