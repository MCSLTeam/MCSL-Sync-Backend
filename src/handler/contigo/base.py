from ...utils import GitHubReleaseSerializer, SyncLogger, update_database


class ContigoReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(owner="djoveryde", repo="Contigo")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Contigo"
            release["mc_version"] = "1.7.10"
            release["core_version"] = release["tag_name"].replace("1.7.10-", "")
            release.pop("tag_name")
            release.pop("target_commitish")
            release.pop("name")
            if release.get("download_url", None) is None:
                self.release_list.remove(release)

        contigo_res = await self.sort_by_mc_versions()

        for mc_version, builds in contigo_res.items():
            update_database("runtime", "Contigo", mc_version, builds=builds)
        SyncLogger.success("Contigo | All versions were loaded.")

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