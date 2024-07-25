from .base import GeyserLoader
from ...utils import SyncLogger


async def geysermc_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = GeyserLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

    SyncLogger.info(
        f"GeyserMC | Elpased time: {time.perf_counter() - start:.2f}s."
    )
