from ...utils import JenkinsCISerializer, cfg, SyncLogger
from asyncio import create_task


class PufferfishCISerializer(JenkinsCISerializer):
    def __init__(self):
        super().__init__(end_point="https://ci.pufferfish.host")
        self.job_list: list[str] = []
        self.job_data: dict = {}

    async def load(self) -> None:
        self.job_list = await self.get_jobs()
        await self.serialize_project_name()

    async def serialize_project_name(self) -> None:
        # print(self.job_list)
        for job in self.job_list:
            if "-Purpur-" in job["name"]:
                '''
                log:
                11 Pufferfish-Purpur-1.17  (deleted)
                Pufferfish
                Pufferfish
                Pufferfish
                Pufferfish
                Pufferfish-Purpur-1.18  (wtf)
                PufferfishPlus
                PufferfishPlusPurpur
                PufferfishPlus
                PufferfishPlusPurpur
                PufferfishPlus
                '''
                print(11, job["name"])
                self.job_list.remove(job)
                continue
            if "Purpur" not in job["name"]:
                # Pufferfish / Pufferfish+
                job["name"], job["major_version"] = job["name"].split("-")
                continue
            elif job["name"].endswith("-Purpur"):
                # Pufferfish+ (Purpur)
                name_list = job["name"].split("-")
                job["name"] = str(name_list[0] + name_list[2])
                job["major_version"] = name_list[1]
                continue
            else:
                continue
        for i in self.job_list:
            print(i["name"])
        # print(self.job_list)

    async def load_versions(self) -> None:
        if not cfg.get("fast_loading"):
            for job in self.job_list:
                await self.load_single_version(job)
        else:
            tasks = [
                create_task(self.load_single_version(job)) for job in self.job_list
            ]
            for task in tasks:
                await task
            del tasks

    @SyncLogger.catch
    async def load_single_version(self, job: str) -> list[dict[str, str]]:
        job_name = job["url"].replace(self.end_point, "").replace("/job/", "")[:-1]
        tmp_data = await self.load_single_job(job_name=job_name)
        from datetime import datetime
        self.job_data[job["name"]] = []
        self.job_data[job["name"]].append(
            {
                "sync_time": datetime.fromtimestamp(single_data["timestamp"]),
                "download_url": str(
                    job["url"]
                    + str(single_data["number"])
                    + "/artifact/"
                    + single_data["artifacts"]["relativePath"]
                ),
                "core_type": job["name"],
                "mc_version": str(single_data["artifacts"]["fileName"].split("-")[1]),
                "core_version": single_data["number"],
            }
            for single_data in tmp_data
        )
        del datetime
