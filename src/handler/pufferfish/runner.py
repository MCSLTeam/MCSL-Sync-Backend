from .base import PufferfishCISerializer
from ...utils import SyncLogger
from orjson import dumps, OPT_INDENT_2


async def pufferfish_runner() -> None:
    import time

    start = time.perf_counter()

    serializer = PufferfishCISerializer()
    await serializer.load()
    await serializer.load_versions()
    for name, data in serializer.job_data.items():
        with open(f"data/core_info/{name}.json", "wb+") as f:
            f.write(dumps(data, option=OPT_INDENT_2))
        SyncLogger.info(f"{name} | All versions were loaded.")

    SyncLogger.info(
        f"Pufferfish | Elpased time: {time.perf_counter() - start:.2f}s."
    )
