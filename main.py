import asyncio
from src.completion_handler import (
    leavesmc_runner,
    papermc_runner,
    arclight_powered_runner,
    catserver_runner,
    sponge_powered_runner,
    bungeecord_runner,
)
from src.utils import cfg, SyncLogger
from os import makedirs
import sys

async def update_default():
    coroutine_list = [
        papermc_runner,
        arclight_powered_runner,
        catserver_runner,
        sponge_powered_runner,
        bungeecord_runner,
    ]
    if cfg.get("fast_loading"):
        tasks = [asyncio.create_task(coroutine()) for coroutine in coroutine_list]
        for task in tasks:
            await task
    else:
        for coroutine in coroutine_list:
            await coroutine()

async def update_leavesmc():
    if cfg.get("fast_loading"):
        await asyncio.create_task(leavesmc_runner())
    else:
        await leavesmc_runner()


if __name__ == "__main__":
    makedirs("data/core_info", exist_ok=True)
    if "--update-default" in sys.argv:
        asyncio.run(update_default())
    if "--update-leaves" in sys.argv:
        SyncLogger.warning("GFW causes the API of LeavesMC to be unstable. Please wait patiently.")
        asyncio.run(update_default())