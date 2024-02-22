from .network import get_json

class JenkinsCISerializer:
    def __init__(self, end_point: str):
        self.end_point = end_point
    async def get_jobs(self) -> list[dict[str, str]]:
        tmp_jobs = await get_json(f"{self.end_point}/api/json?tree=jobs[name,url]")  # type: dict[str, str]
        return [
            {key: value for key, value in job.items() if key != "_class"}
            for job in tmp_jobs["jobs"]
        ]


    async def get_builds(self, job_name: str) -> list[dict[str, str]]:
        tmp_builds = await get_json(
            f"{self.end_point}/job/{job_name}/api/json?tree=builds[number,status,result,artifacts[fileName,relativePath]]"
        )  # type: dict[str, str]
        return [
            {
                key: value
                for key, value in build.items()
                if key != "_class" and build.get("result") == "SUCCESS"
            }
            for build in tmp_builds["builds"]
        ]
