from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ImageIngestionConfig:
    root_dir : str
    database_path : str
    image_dir : str
