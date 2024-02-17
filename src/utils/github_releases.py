from .network import get_json


class GitHubReleaseSerializer(object):
    def __init__(self, user: str, repo: str) -> None:
        self.api_link = "https://api.github.com/repos/{user}/{repo}/releases".format(
            user=user, repo=repo
        )
        self.release_list: list[dict] = []

    async def get_release_data(self) -> None:
        tmp_data = await get_json(self.api_link)
        for data in tmp_data:
            self.release_list.append(
                {
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
