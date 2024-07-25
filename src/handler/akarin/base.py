from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class AkarinReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="Akarin-project", repo="Akarin")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Akarin"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("-")
            )
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)

        akarin_res = await self.sort_by_mc_versions()

        for mc_version, builds in akarin_res.items():
            update_database("runtime", "Akarin", mc_version, builds=builds)
        SyncLogger.success("Akarin | All versions were loaded.")
