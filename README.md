# MCSL-Sync

A tool for synchronizing Minecraft server core files.

## Available Core List

- Arclight
- Banner
- BungeeCord
- CatServer
- Folia
- Leaves
- Lightfall
- Lightfall Client
- Mohist
- Paper
- Pufferfish
- Pufferfish+
- Pufferfish+ (Purpur)
- SpongeForge
- SpongeVanilla
- Travertine
- Velocity
- Waterfall
- Craftbukkit
- Spigot
- Vanilla
- Purpur
- Purformance
- Fabric
- Forge
- Akarin
- NukkitX
- Thermos
- Contigo
- Luminol
- LightingLuminol

## Things to do next
- File hash fetch
- File size calculation

## Command Usage

```bash
Usage: main.py [-h] [-v] [-cl] [-u] [-i] [-s] [-o] [-n ADD_NODE]

Options:
  -h, --help            show this help message and exit
  -v, --version         Show version of MCSL-Sync
  -cl, --core-list      Show available core list
  -u, --update          Update core list
  -i, --init            Init MCSL-Sync configuration
  -s, --server          Run MCSL-Sync API server
  -o, --optimize        Optimize Database
  -n ADD_NODE, --add-node ADD_NODE
                        Add MCSL-Sync-Nodeside Client
```
