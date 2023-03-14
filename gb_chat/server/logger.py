import sys
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter, getLogger
import os

DEBUG = os.getenv("DEBUG", "")
DEBUG = True if "1" == DEBUG or "true" == DEBUG.lower() else False

FORMATTER = Formatter("[%(asctime)s]-[%(levelname)s]-[%(module)s]: %(message)s")
ENCODING = "utf-8"
FILE = "server-gb_async-chat.log"
NAME = "Server"
LEVEL = "INFO"
INTERVAL = 1
PERIOD = "D"
FILE_SUFFIX = "%Y-%m-%d"


# Формат имени файлов при ротации теряет расширение ".log", с помощью этой функции мы меняем стандартное имя на свое
def get_filename(filename):
    log_directory = os.path.split(filename)[0]
    date = os.path.splitext(filename)[1][1:]
    filename = os.path.join(log_directory, date)

    if not os.path.exists("{}.log".format(filename)):
        return "{}.log".format(filename)

    index = 0
    f = "{}.{}.log".format(filename, index)
    while os.path.exists(f):
        index += 1
        f = "{}.{}.log".format(filename, index)
    return f


handler = TimedRotatingFileHandler(FILE, when=PERIOD, interval=INTERVAL, encoding=ENCODING)
handler.suffix = FILE_SUFFIX
handler.namer = get_filename
handler.setFormatter(FORMATTER)

logger = getLogger(NAME)
logger.addHandler(handler)
if DEBUG:
    logger.setLevel("DEBUG")
else:
    logger.setLevel(LEVEL)


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        # не использовал inspect потому что при, обертки метода и функции результаты будут отличаться
        logger.debug("Функция {name} вызвана из функции {caller}".format(
            name=wrap.__name__, caller=sys._getframe(1).f_code.co_name)
        )
        return func(*args, **kwargs)
    return wrap
