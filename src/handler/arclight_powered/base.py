from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


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
            release["core_version"] = "build" + release["core_version"]
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        arclight_res = await self.sort_by_mc_versions()

        for mc_version, builds in arclight_res.items():
            update_database("runtime", "Arclight", mc_version, builds=builds)
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
            release["core_version"] = "build" + release["core_version"]
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        lightfall_res = await self.sort_by_mc_versions()
        for mc_version, builds in lightfall_res.items():
            update_database("runtime", "Lightfall", mc_version, builds=builds)
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
            release["core_version"] = "build" + release["core_version"]
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")

        lightfall_client_res = await self.sort_by_mc_versions()
        for mc_version, builds in lightfall_client_res.items():
            update_database("runtime", "LightfallClient", mc_version, builds=builds)
        SyncLogger.success("LightfallClient | All versions were loaded.")
