from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class ThermosReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="CyberdyneCC", repo="Thermos")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Thermos"
            release["mc_version"] = "1.7.10"
            release["core_version"] = "build" + release["tag_name"]
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)

        thermos_res = await self.sort_by_mc_versions()

        for mc_version, builds in thermos_res.items():
            update_database("runtime", "Thermos", mc_version, builds=builds)
        SyncLogger.success("Thermos | All versions were loaded.")

    @SyncLogger.catch
    async def load_assets(self) -> None:
        for release in self.release_list:
            for asset in release["assets"]:
                if asset["name"] == "libraries.zip":
                    continue
                else:
                    release["download_url"] = (
                        "https://github.moeyy.xyz/" + asset["browser_download_url"]
                    )
            release.pop("assets")