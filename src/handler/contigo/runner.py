from .base import ContigoReleaseSerializer
from ...utils import SyncLogger
from asyncio import create_task


async def contigo_runner() -> None:
    import time

    start = time.perf_counter()
    await create_task(ContigoReleaseSerializer().get_assets())

    SyncLogger.info(f"Contigo | Elpased time: {time.perf_counter() - start:.2f}s.")
