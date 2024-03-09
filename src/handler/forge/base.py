from ...utils import get_json
from asyncio import create_task
from orjson import dumps, OPT_INDENT_2

class ForgeLoader:
    def __init__(self):
        self.mc_version_list: list = []
        self.total_info: dict[str, str] = {}

    async def load_self(self):
        self.mc_version_list = await get_json(
            "https://bmclapi2.bangbang93.com/forge/minecraft"
        )
        tasks = [
            create_task(self.fetch_single_mc_version(mc_version=mc_version))
            for mc_version in self.mc_version_list
        ]
        for task in tasks:
            await task
        del tasks, self.mc_version_list
        with open("data/core_info/Forge.json", "wb+") as f:
            f.write(dumps(self.total_info, option=OPT_INDENT_2))

    async def fetch_single_mc_version(self, mc_version: str):
        tmp_info = await get_json(
            f"https://bmclapi2.bangbang93.com/forge/minecraft/{mc_version}"
        )
        self.total_info[mc_version] = []
        self.total_info[mc_version] = [await create_task(self.serialize_single_build(build)) for build in tmp_info]
        del tmp_info

    async def serialize_single_build(self, single_info: dict):
        return {
            "sync_time": single_info["modified"][:-5] + "Z",
            "download_url": f"https://bmclapi2.bangbang93.com/maven/net/minecraftforge/forge/{single_info['mcversion']}-{single_info['version']}/forge-{single_info['mcversion']}-{single_info['version']}-installer.jar",
            "core_type": "Forge",
            "mc_version": single_info["mcversion"],
            "core_version": single_info["version"],
        }
