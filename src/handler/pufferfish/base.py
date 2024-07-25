from ...utils import JenkinsCISerializer, SyncLogger
from asyncio import create_task


class PufferfishCISerializer(JenkinsCISerializer):
    def __init__(self):
        super().__init__(end_point="https://ci.pufferfish.host")
        self.job_list: list[str] = []
        self.job_data: dict = {}

    async def load(self) -> None:
        await self.serialize_project_name(await self.get_jobs())

    async def serialize_project_name(self, tmp_job_list: list[str]) -> None:
        for job in tmp_job_list:
            if "-Purpur-" in job["name"]:
                continue
            if "Purpur" not in job["name"]:
                # Pufferfish / Pufferfish+
                job["name"], job["major_version"] = job["name"].split("-")
                if "Plus" in job["name"]:
                    job["name"] = job["name"].replace("Plus", "+")
                self.job_list.append(job)
                continue
            elif job["name"].endswith("-Purpur"):
                # Pufferfish+ (Purpur)
                name_list = job["name"].split("-")
                job["name"] = str(name_list[0] + name_list[2]).replace("Plus", "+")
                job["major_version"] = name_list[1]
                self.job_list.append(job)
                continue
            else:
                continue

    async def load_versions(self) -> None:
        tasks = [
            create_task(self.load_single_version(job)) for job in self.job_list
        ]
        for task in tasks:
            await task
        del tasks

    @SyncLogger.catch
    async def load_single_version(self, job: dict) -> list[dict[str, str]]:
        job_name = job["url"].replace(self.end_point, "").replace("/job/", "")[:-1]
        tmp_data = await self.load_single_job(job_name=job_name)
        from time import strftime, localtime

        self.job_data[job["name"]] = {}
        for single_data in tmp_data:
            if not len(single_data):
                continue
            else:
                for artifact in single_data["artifacts"]:
                    self.job_data[job["name"]][
                        str(
                            artifact["fileName"]
                            .replace("paperclip-", "")
                            .removesuffix(".jar")
                            .split("-")[1]
                        )
                    ] = []
        for single_data in tmp_data:
            if not len(single_data):
                continue
            else:
                for artifact in single_data["artifacts"]:
                    self.job_data[job["name"]][
                        str(
                            artifact["fileName"]
                            .replace("paperclip-", "")
                            .removesuffix(".jar")
                            .split("-")[1]
                        )
                    ].append(
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
                                + str(single_data["number"])
                                + "/artifact/"
                                + artifact["relativePath"]
                            ),
                            "core_type": job["name"],
                            "mc_version": str(
                                artifact["fileName"]
                                .replace("paperclip-", "")
                                .removesuffix(".jar")
                                .split("-")[1]
                            ),
                            "core_version": str("build" + str(single_data["number"])),
                        }
                    )
        del strftime, localtime
