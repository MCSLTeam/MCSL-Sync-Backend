import asyncio
from src.handler import (
    leavesmc_runner,
    papermc_runner,
    arclight_powered_runner,
    catserver_runner,
    sponge_powered_runner,
    bungeecord_runner,
    pufferfish_runner,
    mohistmc_runner,
    getbukkit_runner,
    purpurmc_runner,
)
from src.utils import cfg, SyncLogger, init_settings
from src import __version__
import sys

available_core = """
ArclightPowered
├─Arclight
├─Lightfall
└─Lightfall Client
MohistMC
├─Banner
└─Mohist
SpigotMC
├─Spigot
└─BungeeCord
LeavesMC
└─Leaves
Pufferfish
├─Pufferfish
├─Pufferfish+
└─Pufferfish+ (Purpur)
SpongePowered
├─SpongeForge
└─SpongeVanilla
PaperMC
├─Paper
├─Folia
├─Travertine
├─Velocity
└─Waterfall
PurpurMC
└─Purpur
CatServer
CraftBukit
Vanilla"""


async def update_default():
    coroutine_list = [
        leavesmc_runner,
        papermc_runner,
        arclight_powered_runner,
        catserver_runner,
        sponge_powered_runner,
        bungeecord_runner,
        pufferfish_runner,
        mohistmc_runner,
        getbukkit_runner,
        purpurmc_runner,
    ]
    if cfg.get("fast_loading"):
        tasks = [asyncio.create_task(coroutine()) for coroutine in coroutine_list]
        for task in tasks:
            await task
    else:
        for coroutine in coroutine_list:
            await coroutine()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--version",
        "-v",
        help="Show version of MCSL-Sync",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--core-list",
        "-cl",
        help="Show available core list",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--update-default",
        "-ud",
        help="Update default core list",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if not any(value for key, value in args.__dict__.items()):
        parser.error("No argument was specified.")

    init_settings()
    if args.version:
        print(__version__)
    if args.core_list:
        SyncLogger.success(available_core)
    if args.update_default:
        asyncio.run(update_default())

    sys.exit(0)
