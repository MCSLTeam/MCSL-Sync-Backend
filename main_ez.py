import asyncio
from src.handler import (
    arclight_powered_runner,
    catserver_runner,
    sponge_powered_runner,
    bungeecord_runner,
    pufferfish_runner,
    getbukkit_runner,
    leavesmc_runner,
    nukkitx_runner,
    akarin_runner,
    thermos_runner,
    contigo_runner,
    luminol_runner,
    geysermc_runner,
)
from src.utils import SyncLogger, init_settings, read_settings, argument_parser
from src import __version__
from src.api import start_production_server
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
├─Purpur
└─Purformance
LuminolMC
├─Luminol
└─LightingLuminol
GeyserMC
├─Geyser
└─Floodgate
NukkitX
Thermos
Contigo
Akarin
CatServer
Craftbukkit
Vanilla
Fabric
Forge"""


async def update_default():
    tasks = [
        asyncio.create_task(bungeecord_runner()),
        asyncio.create_task(arclight_powered_runner()),
        asyncio.create_task(catserver_runner()),
        asyncio.create_task(akarin_runner()),
        asyncio.create_task(sponge_powered_runner()),
        asyncio.create_task(pufferfish_runner()),
        asyncio.create_task(getbukkit_runner()),
        asyncio.create_task(leavesmc_runner()),
        asyncio.create_task(nukkitx_runner()),
        asyncio.create_task(thermos_runner()),
        asyncio.create_task(contigo_runner()),
        asyncio.create_task(luminol_runner()),
        asyncio.create_task(geysermc_runner()),
    ]
    for task in tasks:
        await task


if __name__ == "__main__":
    args = argument_parser.parse_args()
    if not any(value for _, value in args.__dict__.items()):
        argument_parser.error("No argument was specified.")

    if args.init:
        init_settings()
    if args.server:
        read_settings()
        start_production_server()
    if args.version:
        print(__version__)
    if args.core_list:
        SyncLogger.success(available_core)
    if args.update:
        asyncio.run(update_default())
    if args.optimize:
        from src.utils import optimize_core_data
        asyncio.run(optimize_core_data())
    if args.add_node:
        from src.utils import add_node
        add_node(args.add_node)

    sys.exit(0)
