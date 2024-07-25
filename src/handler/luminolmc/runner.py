from .base import (
    LuminolReleaseSerializer,
    LightingLuminolReleaseSerializer,
    GitHubReleaseSerializer,
)
from ...utils import SyncLogger
from asyncio import create_task


async def luminol_runner() -> None:
    import time

    start = time.perf_counter()
    serializer_list: list[GitHubReleaseSerializer] = [
        LuminolReleaseSerializer(),
        LightingLuminolReleaseSerializer(),
    ]
    tasks = [create_task(parser.get_assets()) for parser in serializer_list]
    for task in tasks:
        await task
    del tasks

    SyncLogger.info(
        f"LuminolMC | Elpased time: {time.perf_counter() - start:.2f}s."
    )
