from .base import PufferfishCISerializer
from ...utils import SyncLogger, cfg
from orjson import dumps, OPT_INDENT_2

async def pufferfish_runner() -> None:
    import time

    start = time.perf_counter()

    serializer = PufferfishCISerializer()
    await serializer.load()
    await serializer.load_versions()
    # print(serializer.job_data)
    # for name, data in serializer.job_data.items():
    #     with open(f"data/core_info/{name}.json", "wb+") as f:
    #         f.write(dumps(data, option=OPT_INDENT_2))
    #     SyncLogger.info(f"{name} | All versions were loaded.")

    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"Pufferfish | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
