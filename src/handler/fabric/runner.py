from ...utils import SyncLogger, update_database
from asyncio import create_task
from .base import FabricParser


async def fabric_runner() -> None:
    import time

    start = time.perf_counter()

    await create_task((parser := FabricParser()).load_self())

    for mc_version, builds in parser.total_info.items():
        update_database("runtime", "Fabric", mc_version, builds=builds)
    SyncLogger.info(f"Fabric | Elpased time: {time.perf_counter() - start:.2f}s.")
