from ...utils import SyncLogger
from asyncio import create_task
from .base import FabricParser
from orjson import dumps, OPT_INDENT_2


async def fabric_runner() -> None:
    import time

    start = time.perf_counter()

    await create_task((parser := FabricParser()).load_self())

    with open(
        "data/core_info/Fabric.json",
        "wb+",
    ) as f:
        f.write(dumps(parser.total_info, option=OPT_INDENT_2))
    SyncLogger.info(f"Fabric | Elpased time: {time.perf_counter() - start:.2f}s.")
