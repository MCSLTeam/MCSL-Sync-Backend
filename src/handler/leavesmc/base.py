from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class LeavesReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="LeavesMC", repo="Leaves")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Leaves"
            release["mc_version"] = release["tag_name"].split("-")[0]
            release["core_version"] = "build" + release["name"].split("-")[1]
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)

        leaves_res = await self.sort_by_mc_versions()

        for mc_version, builds in leaves_res.items():
            update_database("runtime", "Leaves", mc_version, builds=builds)
        SyncLogger.success("Leaves | All versions were loaded.")