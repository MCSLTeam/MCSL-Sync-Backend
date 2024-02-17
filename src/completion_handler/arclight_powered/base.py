from ...utils import GitHubReleaseSerializer, SyncLogger
from pandas import DataFrame
from orjson import dumps, OPT_INDENT_2


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

        arclight_res = await self.sort_by_mc_versions()
        with open("data/ArclightPowered/Arclight.json", "wb+") as f:
            f.write(dumps(arclight_res, option=OPT_INDENT_2))
        SyncLogger.success("ArclightPowered | Arclight | All versions were loaded.")

    async def sort_by_mc_versions(self) -> list:
        data_frame = DataFrame(self.release_list)
        groups = data_frame.groupby("mc_version").groups
        res = []
        for version, indices in groups.items():
            res.append({version: data_frame.loc[indices].to_dict("records")})
        return res
