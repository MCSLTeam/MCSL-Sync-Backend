from ...utils import SyncLogger, cfg
from .base import GetBukkitParser
from asyncio import create_task


async def getbukkit_runner() -> None:
    import time

    start = time.perf_counter()

    parser_list: list[GetBukkitParser] = [
        GetBukkitParser(core_type="craftbukkit"),
        GetBukkitParser(core_type="spigot"),
        GetBukkitParser(core_type="vanilla"),
    ]
    if not cfg.get("fast_loading"):
        tasks = []
        for parser in parser_list:
            await parser.get_version_list()
        for task in tasks:
            await task
        del tasks
    else:
        tasks = [create_task(parser.get_version_list()) for parser in parser_list]
        for task in tasks:
            await task
        del tasks

    SyncLogger.info(
        f"GetBukkit | Elpased time: {time.perf_counter() - start:.2f}s. (Fast load {'enabled' if cfg.get('fast_loading') else 'disabled'})"
    )
