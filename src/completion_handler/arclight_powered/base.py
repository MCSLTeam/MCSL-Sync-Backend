from ...utils import GitHubReleaseSerializer, SyncLogger

from orjson import dumps, OPT_INDENT_2


class ArclightReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="IzzelAliz", repo="Arclight")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Arclight"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("/")
            )
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        arclight_res = await self.sort_by_mc_versions()
        with open("data/core_info/Arclight.json", "wb+") as f:
            f.write(dumps(arclight_res, option=OPT_INDENT_2))
        SyncLogger.success("Arclight | All versions were loaded.")


class LightfallReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="ArclightPowered", repo="lightfall")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Lightfall"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("-")
            )
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        lightfall_res = await self.sort_by_mc_versions()
        with open("data/core_info/Lightfall.json", "wb+") as f:
            f.write(dumps(lightfall_res, option=OPT_INDENT_2))
        SyncLogger.success("Lightfall | All versions were loaded.")


class LightfallClientReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="ArclightPowered", repo="lightfall-client")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "LightfallClient"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("-")
            )
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        lightfall_client_res = await self.sort_by_mc_versions()
        with open("data/core_info/LightfallClient.json", "wb+") as f:
            f.write(dumps(lightfall_client_res, option=OPT_INDENT_2))
        SyncLogger.success("LightfallClient | All versions were loaded.")
