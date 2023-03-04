from logging import Formatter, FileHandler, getLogger
import os

DEBUG = os.getenv("DEBUG")
DEBUG = True if "1" == DEBUG or "true" == DEBUG.lower() else False

FORMATTER = Formatter("[%(asctime)s]-[%(levelname)s]-[%(module)s]: %(message)s")
ENCODING = "utf-8"
NAME = "Server"
LEVEL = "INFO"
FILE = "client-gb_async-chat.log"

handler = FileHandler(FILE, encoding=ENCODING)
handler.setFormatter(FORMATTER)

logger = getLogger(NAME)
logger.addHandler(handler)
if DEBUG:
    logger.setLevel("DEBUG")
else:
    logger.setLevel(LEVEL)
