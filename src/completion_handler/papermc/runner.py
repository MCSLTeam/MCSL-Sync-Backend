from .base import PaperLoader
from ...utils import SyncLogger, cfg
from os import makedirs

async def papermc_runner() -> None:
    SyncLogger.info("PaperMC | Loading components...")
    import time
    makedirs("data/PaperMC", exist_ok=True)
    start = time.perf_counter()
    project_list = PaperLoader()
    await project_list.load_self()
    await project_list.load_all_projects()
    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"PaperMC | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('force_fast_loading') else 'disabled'})"
    )
