import os

from src.common import constants
from src.utils import os_utils


LOCAL_FILE_PATH = os.path.join(constants.LOCAL_BASE_DIR, '.credentials')
DELIMITER = ':'


def read_credentials(key):
    try:
        contents = os_utils.read(LOCAL_FILE_PATH)

        for line in contents.splitlines():
            if key in line:
                key, username, password = line.split(DELIMITER)
                return username, password

        return None, None

    except IOError:
        return None, None


def write_credentials(key, username, password):
    os_utils.write(DELIMITER.join([key, username, password]), LOCAL_FILE_PATH)
