from .base import LeavesLoader
from ...utils import SyncLogger


async def leavesmc_runner() -> None:
    import time

    start = time.perf_counter()

    await LeavesLoader().load_self()

    SyncLogger.info(
        f"LeavesMC | Elpased time: {time.perf_counter() - start:.2f}s."
    )
