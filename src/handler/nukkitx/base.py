from ...utils import JenkinsCISerializer, SyncLogger
from asyncio import create_task


class NukkitXCISerializer(JenkinsCISerializer):
    def __init__(self):
        super().__init__(end_point="https://ci.opencollab.dev/job/NukkitX/job/Nukkit")
        self.job_data: dict = {}

    async def load(self) -> None:
        await create_task(
            self.load_single_version(
                {
                    "name": "NukkitX",
                    "url": "https://ci.opencollab.dev/job/NukkitX/job/Nukkit",
                }
            )
        )

    @SyncLogger.catch
    async def load_single_version(self, job: dict) -> list[dict[str, str]]:
        tmp_data = await self.load_single_job(job_name="master")
        from time import strftime, localtime
        self.job_data["general"] = []
        for single_data in tmp_data:
            if not len(single_data):
                continue
            else:
                if len(single_data["artifacts"]):
                    for artifact in single_data["artifacts"]:
                        self.job_data["general"].append(
                            {
                                "sync_time": str(
                                    strftime(
                                        "%Y-%m-%d %H:%M:%S",
                                        localtime(int(single_data["timestamp"]) / 1000),
                                    )
                                ).replace(" ", "T")
                                + "Z",
                                "download_url": str(
                                    job["url"]
                                    + "/job/master/"
                                    + str(single_data["number"])
                                    + "/artifact/"
                                    + artifact["relativePath"]
                                ),
                                "core_type": job["name"],
                                "mc_version": "general",
                                "core_version": str(
                                    "build" + str(single_data["number"])
                                ),
                            }
                        )
        del strftime, localtime
