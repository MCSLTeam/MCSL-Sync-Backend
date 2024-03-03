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
    fabric_runner,
)
from src.utils import SyncLogger, init_settings, argument_parser
from src import __version__
from src.api import start_api_server
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
Vanilla
Fabric"""


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
        fabric_runner,
    ]
    for coroutine in coroutine_list:
        await coroutine()


if __name__ == "__main__":
    args = argument_parser.parse_args()

    if not any(value for _, value in args.__dict__.items()):
        argument_parser.error("No argument was specified.")

    if args.init:
        init_settings()
    if args.server:
        start_api_server()
    if args.version:
        print(__version__)
    if args.core_list:
        SyncLogger.success(available_core)
    if args.update_default:
        asyncio.run(update_default())

    sys.exit(0)
