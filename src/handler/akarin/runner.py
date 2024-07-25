from .base import AkarinReleaseSerializer
from ...utils import SyncLogger
from asyncio import create_task


async def akarin_runner() -> None:
    import time

    start = time.perf_counter()
    await create_task(AkarinReleaseSerializer().get_assets())

    SyncLogger.info(f"Akarin | Elpased time: {time.perf_counter() - start:.2f}s.")
