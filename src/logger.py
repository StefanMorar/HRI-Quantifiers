import logging
import os

from dotenv import load_dotenv

from utils import string_to_bool

load_dotenv()
is_debug_enabled = os.getenv('IS_DEBUG_ENABLED')

formatter = logging.Formatter('%(asctime)s -  %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')


def setup_logging(debug_enabled):
    custom_logger = logging.getLogger(__name__)

    custom_logger.setLevel(logging.DEBUG if debug_enabled else logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_enabled else logging.INFO)
    console_handler.setFormatter(formatter)

    custom_logger.addHandler(console_handler)

    return custom_logger


def get_logger():
    configuration = string_to_bool(is_debug_enabled)
    return setup_logging(configuration)


logger = get_logger()
