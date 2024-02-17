from .base import CatServerReleaseSerializer
from ...utils import SyncLogger, cfg


async def catserver_runner() -> None:
    import time

    start = time.perf_counter()

    await CatServerReleaseSerializer().get_assets()

    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"CatServer | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
