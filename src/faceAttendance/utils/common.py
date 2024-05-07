import os
from box.exceptions import BoxValueError
import yaml
from faceAttendance import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import base64

@ensure_annotations
def read_yaml(file_path: Path) -> ConfigBox:
    try:
        with open(file_path, 'r') as f:
            contents = yaml.safe_load(f)
            logger.info(f"Loaded yaml file {file_path}")
            return ConfigBox(contents)
        
    except BoxValueError:
        raise ValueError(f'yaml file {file_path} does not exist or given invalid')
    
    except IOError as e:
        raise e
    

def create_dirs(dirs: List[str], verbose: bool=True):

    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        if verbose:
            logger.info(f'Creating directory {dir}')


@ensure_annotations
def load_json(file_path: Path) -> ConfigBox:
    with open(file_path, 'r') as f:
        content = ConfigBox(json.load(f))
    logger.info(f'Json file loaded {file_path}')

    return content


@ensure_annotations
def save_json(data:Dict, file_path: Path) :
    with open(file_path, 'w') as jf:
        json.dump(data, jf, indent=4)

    logger.info(f'Data saved in {file_path} json file')


@ensure_annotations
def load_bin(file_path: Path) -> Any:
    with open(file_path, 'rb') as bf:
        data = joblib.load(file_path)
    logger.info(f'Data binary file {file_path} loaded')

    return data

@ensure_annotations
def save_bin(data:Any, file_path:Path):
    with open(file_path, 'w') as bf:
        joblib.dump(data, bf)

    logger.info(f'Data saved in {file_path} binary file')


@ensure_annotations
def get_size(file_path: Path) -> str:
    size_in_KB = round(os.path.getsize(file_path)/1024)
    return f'--{size_in_KB} KB'


def decode_image(img_string, file_path):
    img_data = base64.b64decode(img_string)
    with open(file_path, 'w') as img:
        img.write(img_data)
        img.close()


def encode_image(file_path):
    with open(file_path, 'rb') as img:
        img_string = base64.b64encode(img.read())
    
    return img_string