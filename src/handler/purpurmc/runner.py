from .base import PurpurLoader
from ...utils import SyncLogger, cfg


async def purpurmc_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = PurpurLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

    SyncLogger.info(
        f"PurpurMC | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
