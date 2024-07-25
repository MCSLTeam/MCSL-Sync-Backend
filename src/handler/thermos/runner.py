from .base import ThermosReleaseSerializer
from ...utils import SyncLogger
from asyncio import create_task


async def thermos_runner() -> None:
    import time

    start = time.perf_counter()
    await create_task(ThermosReleaseSerializer().get_assets())

    SyncLogger.info(f"Thermos | Elpased time: {time.perf_counter() - start:.2f}s.")
