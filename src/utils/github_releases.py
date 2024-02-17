from .network import get_json
from pandas import DataFrame

class GitHubReleaseSerializer(object):
    def __init__(self, owner: str, repo: str) -> None:
        self.api_link = "https://api.github.com/repos/{user}/{repo}/releases".format(
            user=owner, repo=repo
        )
        self.release_list: list[dict] = []

    async def get_release_data(self) -> None:
        tmp_data = await get_json(self.api_link)
        for data in tmp_data:
            self.release_list.append(
                {
                    "target_commitish": data["target_commitish"],
                    "name": data["name"],
                    "tag_name": data["tag_name"],
                    "sync_time": data["published_at"],
                    "assets": data["assets"],
                }
            )
        await self.load_assets()

    async def load_assets(self) -> None:
        for release in self.release_list:
            for asset in release["assets"]:
                release["download_url"] = "https://github.moeyy.xyz/" + asset["browser_download_url"]
            release.pop("assets")

    async def sort_by_mc_versions(self) -> dict:
        data_frame = DataFrame(self.release_list)
        groups = data_frame.groupby("mc_version").groups
        res = {}
        for version, indices in groups.items():
            res.update({version: data_frame.loc[indices].to_dict("records")})
        return res
