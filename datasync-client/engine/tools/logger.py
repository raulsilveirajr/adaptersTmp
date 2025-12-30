import datetime
import os

from dotenv import load_dotenv

load_dotenv()

class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

LOG_LEVEL = os.getenv("LOG_LEVEL", LogLevel.DEBUG)

def log(
    message: str,
    level: LogLevel = LogLevel.INFO,
):
    log_levels = {
        LogLevel.DEBUG: 0,
        LogLevel.INFO: 1,
        LogLevel.WARNING: 2,
        LogLevel.ERROR: 3,
    }

    if log_levels[level] < log_levels[LOG_LEVEL]:
        return

    print(
        f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {level}: {message}"
    )
