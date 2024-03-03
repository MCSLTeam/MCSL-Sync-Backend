from .base import PaperLoader
from ...utils import SyncLogger


async def papermc_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = PaperLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

    SyncLogger.info(
        f"PaperMC | Elpased time: {time.perf_counter() - start:.2f}s."
    )
