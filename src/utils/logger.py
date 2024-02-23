from loguru import logger

__version__ = "0.1.0"
SyncLogger = logger
SyncLogger.add(
    sink="logs/{time}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
    rotation="1 days",
    compression="gz",
    retention="1 weeks",
)
