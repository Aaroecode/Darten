import logging, os
from typing import Union
from datetime import datetime


def get_logger(name: Union[str, None] = "global", filepath: Union[str, None] = str(os.path.join(os.getcwd(), "logs")), level = logging.DEBUG):


    if not os.path.exists(filepath):
        os.makedirs(filepath, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y_%m_%d %H")
    file_name = f"{timestamp} - log.log"
    file = str(os.path.join(filepath, file_name))
    logging.basicConfig(
        filemode= "a",
        filename = file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger