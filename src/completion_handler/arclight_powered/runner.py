from .base import ArclightReleaseSerializer
from ...utils import SyncLogger, cfg
from orjson import dumps

async def arclight_powered_runner() -> None:
    SyncLogger.info("ArclightPowered | Loading components...")
    import time

    start = time.perf_counter()
    serializer = ArclightReleaseSerializer()
    await serializer.get_assets()
    print(dumps(await serializer.sort_mc_versions()))
    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"ArclightPowered | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('force_fast_loading') else 'disabled'})"
    )
