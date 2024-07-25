from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class LuminolReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="LuminolMC", repo="Luminol")

    async def get_assets(self) -> None:
        await self.get_release_data()
        idx: int = len(self.release_list)
        for release in self.release_list:
            release["core_type"] = "Luminol"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("-")
            )
            release["core_version"] = f"build{idx}"
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)
            idx -= 1

        luminol_res = await self.sort_by_mc_versions()

        for mc_version, builds in luminol_res.items():
            update_database("runtime", "Luminol", mc_version, builds=builds)
        SyncLogger.success("Luminol | All versions were loaded.")


class LightingLuminolReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="LuminolMC", repo="LightingLuminol")

    async def get_assets(self) -> None:
        await self.get_release_data()
        idx: int = len(self.release_list)
        for release in self.release_list:
            release["core_type"] = "LightingLuminol"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("-")
            )
            release["core_version"] = f"build{idx}"
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)
            idx -= 1

        lighting_luminol_res = await self.sort_by_mc_versions()
        for mc_version, builds in lighting_luminol_res.items():
            update_database("runtime", "LightingLuminol", mc_version, builds=builds)
        SyncLogger.success("LightingLuminol | All versions were loaded.")
