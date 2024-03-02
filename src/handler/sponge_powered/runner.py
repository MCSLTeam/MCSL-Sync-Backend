from .base import SpongePoweredLoader
from ...utils import SyncLogger, cfg


async def sponge_powered_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = SpongePoweredLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

    SyncLogger.info(
        f"SpongePowered | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
