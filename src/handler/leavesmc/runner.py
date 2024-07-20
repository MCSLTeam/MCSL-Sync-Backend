from .base import LeavesReleaseSerializer
from ...utils import SyncLogger


async def leavesmc_runner() -> None:
    import time

    start = time.perf_counter()

    await LeavesReleaseSerializer().get_assets()

    SyncLogger.info(
        f"LeavesMC | Elpased time: {time.perf_counter() - start:.2f}s."
    )
