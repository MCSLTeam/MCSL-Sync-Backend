from .base import LeavesLoader
from ...utils import SyncLogger, cfg


async def leavesmc_runner() -> None:
    import time

    start = time.perf_counter()

    await LeavesLoader().load_self()

    SyncLogger.info(
        f"PaperMC | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
