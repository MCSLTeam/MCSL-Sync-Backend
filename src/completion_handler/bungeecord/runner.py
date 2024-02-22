from ...utils import SyncLogger, cfg
from orjson import dumps, OPT_INDENT_2

async def bungeecord_runner() -> None:
    import time

    start = time.perf_counter()

    bungeecord_links = {
        "Latest": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "Latest",
                "core_version": "lastSuccessfulBuild",
            },
        ],
        "1.7.10": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/1119/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.7.10",
                "core_version": "1119",
            },
        ],
        "1.6.4": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/701/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.6.4",
                "core_version": "701",
            },
        ],
        "1.6.2": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/666/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.6.2",
                "core_version": "666",
            },
        ],
        "1.5.2": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/548/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.5.2",
                "core_version": "548",
            },
        ],
        "1.5.0": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/386/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.5.0",
                "core_version": "386",
            },
        ],
        "1.4.7": [
            {
                "sync_time": "1970-01-01T00:00:00.000Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/251/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.4.7",
                "core_version": "251",
            },
        ],
    }

    with open("data/core_info/BungeeCord.json", "wb+") as f:
        f.write(dumps(bungeecord_links, option=OPT_INDENT_2))
    SyncLogger.success("BungeeCord | All versions were loaded.")
    elpased_time = time.perf_counter() - start

    SyncLogger.info(
        f"BungeeCord | Elpased time: {elpased_time:.2f}s. (Force-Fast-Loading {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
