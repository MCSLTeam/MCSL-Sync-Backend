from .base import ArclightReleaseSerializer, LightfallReleaseSerializer
from ...utils import SyncLogger, cfg


async def arclight_powered_runner() -> None:
    import time

    start = time.perf_counter()

    await ArclightReleaseSerializer().get_assets()
    await LightfallReleaseSerializer().get_assets()

    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"ArclightPowered | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
