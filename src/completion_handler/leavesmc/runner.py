from .base import LeavesLoader
from ...utils import SyncLogger, cfg


async def leavesmc_runner() -> None:
    import time

    start = time.perf_counter()

    await LeavesLoader().load_self()

    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"PaperMC | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
