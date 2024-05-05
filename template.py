import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s:%(message)s]')

project_name = 'faceAttendance'
list_files =[
    '.github/workflow/.gitkeep',
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/config/configuration.py',
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/utils/common.py',
    f'src/{project_name}/constants/__init__.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/pipeline/__init__.py',
    'config/config.yaml',
    'dvc.yaml',
    'params.yaml',
    'requirements.txt',
    'setup.py',
    'research/trails.ipynb',
    'README.md',
    'LICENSE',
    'app.py',
    'main.py',
    '.gitignore'
    ]

for file in list_files:
    file_path = Path(file)
    file_dir, file_name = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f'Create directory: {file_dir}')

    if (not os.path.exists(file_path) or (os.path.getsize(file_path) == 0)):
        with open(file_path, 'w'):
            pass
        logging.info(f'Create file: {file_path}')

    else: 
        logging.info(f'{file_name} already exists with size {os.path.getsize(file_path)}')