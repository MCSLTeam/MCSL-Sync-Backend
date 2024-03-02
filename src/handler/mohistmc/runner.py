from .base import MohistLoader
from ...utils import SyncLogger, cfg


async def mohistmc_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = MohistLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

    SyncLogger.info(
        f"MohistMC | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )