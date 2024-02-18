import warnings
import sys
warnings.filterwarnings('ignore', category=UserWarning)
from loguru import logger

log_format = "{time:YYYY-MM-DD at HH:mm:ss} : {message}"
logger.add("logs/info.log", format=log_format, level="INFO")
logger.add("logs/debug.log", format=log_format, level="DEBUG")
logger.add("logs/error.log", format=log_format, level="ERROR")
logger.add("logs/warning.log",  format=log_format, level="WARNING")


from uvicorn import run

from app import app



if __name__ == "__main__":   
    run("main:app", reload=True)