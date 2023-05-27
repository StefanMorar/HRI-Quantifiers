import logging
import os

from dotenv import load_dotenv

load_dotenv()
debugging_enabled = os.getenv('DEBUGGING_ENABLED')

formatter = logging.Formatter('%(asctime)s -  %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')


def string_to_bool(string):
    if string.lower() in ['true', 'yes', '1']:
        return True
    elif string.lower() in ['false', 'no', '0']:
        return False
    else:
        raise ValueError("Invalid boolean string")


def setup_logging(debug_enabled):
    custom_logger = logging.getLogger(__name__)

    custom_logger.setLevel(logging.DEBUG if debug_enabled else logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_enabled else logging.INFO)
    console_handler.setFormatter(formatter)

    custom_logger.addHandler(console_handler)

    return custom_logger


def get_logger():
    configuration = string_to_bool(debugging_enabled)
    return setup_logging(configuration)


logger = get_logger()
