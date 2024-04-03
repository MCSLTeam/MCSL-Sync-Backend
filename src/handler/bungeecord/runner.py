from ...utils import SyncLogger, update_database


async def bungeecord_runner() -> None:
    import time

    start = time.perf_counter()

    bungeecord_links = {
        "Latest": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "Latest",
                "core_version": "lastSuccessfulBuild",
            },
        ],
        "1.7.10": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/1119/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.7.10",
                "core_version": "1119",
            },
        ],
        "1.6.4": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/701/artifact/bootstrap/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.6.4",
                "core_version": "701",
            },
        ],
        "1.6.2": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/666/artifact/proxy/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.6.2",
                "core_version": "666",
            },
        ],
        "1.5.2": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/548/artifact/proxy/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.5.2",
                "core_version": "548",
            },
        ],
        "1.5.0": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/386/artifact/proxy/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.5.0",
                "core_version": "386",
            },
        ],
        "1.4.7": [
            {
                "sync_time": "1970-01-01T00:00:00Z",
                "download_url": "https://ci.md-5.net/job/BungeeCord/251/artifact/proxy/target/BungeeCord.jar",
                "core_type": "BungeeCord",
                "mc_version": "1.4.7",
                "core_version": "251",
            },
        ],
    }

    for mc_version, builds in bungeecord_links.items():
        update_database("runtime", "BungeeCord", mc_version, builds=builds)
    SyncLogger.success("BungeeCord | All versions were loaded.")

    SyncLogger.info(
        f"BungeeCord | Elpased time: {time.perf_counter() - start:.2f}s."
    )
