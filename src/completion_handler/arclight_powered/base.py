from ...utils import GitHubReleaseSerializer
from pandas import DataFrame


class ArclightReleaseSerializer(GitHubReleaseSerializer):
    def __init__(self) -> None:
        super().__init__(user="IzzelAliz", repo="Arclight")

    async def get_assets(self) -> None:
        await self.get_release_data()
        for release in self.release_list:
            release["core_type"] = "Arclight"
            release["mc_version"], release["core_version"] = tuple(
                release["tag_name"].split("/")
            )
            release.pop("tag_name")

    async def sort_mc_versions(self) -> dict:
        data_frame = DataFrame(self.release_list)
        groups = data_frame.groupby("mc_version").groups
        aaa = {}
        for version, indices in groups.items():
            aaa.update({version: data_frame.loc[indices].to_dict("records")})
        return aaa
