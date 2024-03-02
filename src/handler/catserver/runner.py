from .base import CatServerReleaseSerializer
from ...utils import SyncLogger, cfg


async def catserver_runner() -> None:
    import time

    start = time.perf_counter()

    await CatServerReleaseSerializer().get_assets()

    SyncLogger.info(
        f"CatServer | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
