from .base import (
    ArclightReleaseSerializer,
    LightfallReleaseSerializer,
    LightfallClientReleaseSerializer,
    GitHubReleaseSerializer,
)
from ...utils import SyncLogger, cfg
from asyncio import create_task


async def arclight_powered_runner() -> None:
    import time

    start = time.perf_counter()
    serializer_list: list[GitHubReleaseSerializer] = [
        ArclightReleaseSerializer(),
        LightfallReleaseSerializer(),
        LightfallClientReleaseSerializer(),
    ]
    if not cfg.get("fast_loading"):
        tasks = []
        for parser in serializer_list:
            await parser.get_assets()
        for task in tasks:
            await task
        del tasks
    else:
        tasks = [create_task(parser.get_assets()) for parser in serializer_list]
        for task in tasks:
            await task
        del tasks

    SyncLogger.info(
        f"ArclightPowered | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
