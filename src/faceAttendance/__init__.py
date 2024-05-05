import os
import logging
import sys


format_log = '[%(asctime)s - %(levelname)s: %(module)s __ %(message)s]'
log_dir = 'logs'
log_filepath = os.path.join(log_dir,"running_log.log")

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    format=format_log,
                    handlers=[
                        logging.FileHandler(log_filepath),
                        logging.StreamHandler(sys.stdout)]
                    )

logger = logging.getLogger(__name__)