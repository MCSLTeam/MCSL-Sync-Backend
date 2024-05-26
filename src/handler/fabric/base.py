# IMPORTANT： We don't recommend downloading Fabric Installer. Use easier Fabric Excutable Server instead.

from asyncio import create_task
from ...utils.network import get_json


class FabricParser:
    def __init__(self) -> None:
        self.end_point = "https://meta.fabricmc.net/v2/versions"
        self.game_version_list: list = []
        self.fabric_loader_list: list = []
        self.installer_version: str = "1.0.0"
        self.total_info: dict[str, list[dict[str, str]]] = {}

    async def load_self(self) -> None:
        """Load all data."""
        await self.get_latest_installer_version()
        tasks = [create_task(self.load_game_version_list()), create_task(self.load_fabric_loader_list())]
        for task in tasks:
            await task
        del tasks
        await self.serialize_info()

    async def load_game_version_list(self) -> list:
        """
        Get Minecraft version list.
        (We will ignore unstable versions)
        """
        data = await get_json(f"{self.end_point}/game")  # type: list[dict[str, str|bool]]
        self.game_version_list.extend(
            version["version"] for version in data if version.get("stable")
        )

    async def load_fabric_loader_list(self) -> list:
        """Get Fabric Loader version list."""
        data = await get_json(f"{self.end_point}/loader")  # type: list[dict[str, str|bool]]
        self.fabric_loader_list.extend(version["version"] for version in data)

    async def get_latest_installer_version(self) -> None:
        """Get latest installer version."""
        data = await get_json(f"{self.end_point}/installer")
        self.installer_version = [item["version"] for item in data if item["stable"]][0]

    async def serialize_info(self):
        tasks = [create_task(self.serialize_single_version_info(v)) for v in self.game_version_list]
        for task in tasks:
            await task
        del tasks

    async def serialize_single_version_info(self, v: str):
        self.total_info[v] = []
        for loader_version in reversed(self.fabric_loader_list):
            if int(loader_version.split(".")[1]) >=12:
                self.total_info[v].append(
                    {
                        "sync_time": "1970-01-01T00:00:00Z",
                        "download_url": f"https://meta.fabricmc.net/v2/versions/loader/{v}/{loader_version}/{self.installer_version}/server/jar",
                        "core_type": "Fabric",
                        "mc_version": v,
                        "core_version": loader_version,
                    }
                )
            else:
                continue