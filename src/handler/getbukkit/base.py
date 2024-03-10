from datetime import datetime
from lxml import html
from ...utils import SyncLogger, get_text, update_database


class GetBukkitParser:
    def __init__(self, core_type: str):
        self.core_type = core_type

    async def convert_to_ISO8601(self, date_string):
        return (
            datetime.strptime(date_string, "%A, %B %d %Y")
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .isoformat()
            + "Z"
        )

    async def get_version_list(self):
        root = html.fromstring(
            await get_text(f"https://getbukkit.org/download/{self.core_type}")
        )

        versions = {}

        download_panes = root.xpath('//div[@class="download-pane"]')
        for pane in download_panes:
            version = pane.xpath(".//h2/text()")[0]
            sync_time = pane.xpath(".//h3/text()")[1]

            versions[version.strip()] = []

            versions[version.strip()].append(
                {
                    "sync_time": await self.convert_to_ISO8601(sync_time.strip()),
                    "download_url": await self.get_real_download_link(
                        pane.xpath('.//a[@class="btn btn-download"]/@href')[0]
                    ),
                    "core_type": self.core_type.capitalize(),
                    "mc_version": version.strip(),
                    "core_version": "Latest",
                }
            )
        await self.save_data(versions)

    async def get_real_download_link(self, url):
        return html.fromstring(await get_text(url)).xpath(
            '//div[@class="well"]//h2/a/@href'
        )[0]

    async def save_data(self, data_dict: dict):
        for mc_version, builds in data_dict.items():
            update_database("runtime", self.core_type.capitalize(), mc_version, builds=builds)
        SyncLogger.success(f"{self.core_type.capitalize()} | All versions were loaded.")
