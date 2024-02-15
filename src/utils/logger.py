from loguru import logger

SyncLogger = logger

SyncLogger.add(
    sink="logs/latest.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
    rotation="5 MB",
    compression="zip",
    retention="10 days",
)
SyncLogger.info("MCSL Sync Core is loading...")