from .base import NukkitXCISerializer
from ...utils import SyncLogger, update_database


async def nukkitx_runner() -> None:
    import time

    start = time.perf_counter()

    serializer = NukkitXCISerializer()
    await serializer.load()
    for mc_version, builds in serializer.job_data.items():
        update_database("runtime", "NukkitX", mc_version, builds=builds)
    SyncLogger.success("NukkitX | All versions were loaded.")

    SyncLogger.info(f"NukkitX | Elpased time: {time.perf_counter() - start:.2f}s.")
