from .base import PaperLoader
from ...utils import SyncLogger, cfg


async def papermc_runner() -> None:
    SyncLogger.info("PaperMC | Loading components...")
    import time

    start = time.perf_counter()
    project_list = PaperLoader()
    await project_list.load_self()
    await project_list.load_all_projects()
    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"PaperMC | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('force_fast_loading') else 'disabled'})"
    )
