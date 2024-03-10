from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class CatServerReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="Luohuayu", repo="CatServer")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "CatServer"
            release["mc_version"] = release["target_commitish"]
            release["core_version"] = release["tag_name"]
            release.pop("tag_name")
            release.pop("name")
            release.pop("target_commitish")

        catserver_res = await self.sort_by_mc_versions()
        for mc_version, builds in catserver_res.items():
            update_database("runtime", "CatServer", mc_version, builds=builds)
        SyncLogger.success("CatServer | All versions were loaded.")
