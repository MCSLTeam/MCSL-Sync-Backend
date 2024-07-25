import asyncio
from src.handler import forge_runner
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
        asyncio.create_task(forge_runner()),
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
