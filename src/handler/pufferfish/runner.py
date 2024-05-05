from .base import PufferfishCISerializer
from ...utils import SyncLogger, update_database


async def pufferfish_runner() -> None:
    import time

    start = time.perf_counter()

    serializer = PufferfishCISerializer()
    await serializer.load()
    await serializer.load_versions()
    for name, data in serializer.job_data.items():
        for mc_version, builds in data.items():
            update_database("runtime", name, mc_version, builds=builds)
        SyncLogger.success(f"{name} | All versions were loaded.")

    SyncLogger.info(f"Pufferfish | Elpased time: {time.perf_counter() - start:.2f}s.")
