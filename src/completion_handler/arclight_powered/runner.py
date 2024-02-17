from .base import ArclightReleaseSerializer
from ...utils import SyncLogger, cfg
from os import makedirs


async def arclight_powered_runner() -> None:
    SyncLogger.info("ArclightPowered | Loading components...")
    import time

    makedirs("data/ArclightPowered", exist_ok=True)
    start = time.perf_counter()
    await ArclightReleaseSerializer().get_assets()
    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"ArclightPowered | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('force_fast_loading') else 'disabled'})"
    )
