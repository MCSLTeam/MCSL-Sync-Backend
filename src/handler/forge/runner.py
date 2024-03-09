from .base import ForgeLoader
from ...utils import SyncLogger


async def forge_runner() -> None:
    import time

    start = time.perf_counter()

    project_list = ForgeLoader()
    await project_list.load_self()

    SyncLogger.info(f"Forge | Elpased time: {time.perf_counter() - start:.2f}s.")
