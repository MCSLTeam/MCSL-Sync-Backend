from ...utils import get_json, SyncLogger, update_database
from traceback import format_exception
from asyncio import create_task
from time import localtime, strftime


class _ProjectList(object):
    def __init__(self) -> None:
        self.project_id_list: list = []
        self.project_list: list = []

    async def load_self(self, retry: int = 0) -> None:
        # fmt: off
        if retry:
            SyncLogger.warning("MohistMC | Retrying getting project list...")
        self.project_id_list = await get_json("https://mohistmc.com/api/v2/projects/")  # noqa: E501
        if self.project_id_list is None:
            SyncLogger.error("MohistMC | Project list load failed!")
            return self.load_self(retry=(retry+1))
        # fmt: on

    async def load_all_projects(self) -> None:
        tasks = [
            create_task(self.load_single_project(project_id=project["project"]))
            for project in self.project_id_list
        ]
        for task in tasks:
            await task
        del tasks

    async def load_single_project(self, project_id: str) -> None:
        try:
            p = Project(project_id=project_id)
            await p.load_self()
            self.project_list.append(p)
        except Exception as e:
            SyncLogger.warning(
                "{project_id} | Failed to load project!".format(
                    project_id=project_id.capitalize()
                )
            )
            SyncLogger.error("".join(format_exception(e)))
        SyncLogger.success(
            "{project_id} | All versions were loaded.".format(
                project_id=project_id.capitalize()
            )
        )


class Project(object):
    def __init__(self, project_id: str) -> None:
        self.project_id: str = project_id
        self.project_name: str = project_id.capitalize()
        self.version_label_list: list = []
        self.versions: list[SingleVersion] = []

    async def load_self(self, retry: int = 0) -> None:
        if retry:
            SyncLogger.warning("{project_id} | Retrying getting project info...")
        tmp_data = await get_json(
            "https://mohistmc.com/api/v2/projects/{project_id}/".format(
                project_id=self.project_id
            )
        )  # type: dict

        self.version_label_list = tmp_data.get("versions", None)

        if self.version_label_list is None:
            SyncLogger.error(
                "{project_id} | Project info load failed!".format(
                    project_id=self.project_id.capitalize()
                )
            )
            return self.load_self(retry=(retry + 1))
        await self.load_version_list()

    async def load_version_list(self) -> None:
        tasks = [
            create_task(self.load_single_version(version=version))
            for version in self.version_label_list
        ]
        for task in tasks:
            await task
        del tasks
        dict_info = await self.gather_project()
        for mc_version, builds in dict_info.items():
            update_database("runtime", self.project_name, mc_version, builds=builds)

    async def load_single_version(self, version: str) -> None:
        sv = SingleVersion(
            project_id=self.project_id, project_name=self.project_name, version=version
        )
        try:
            await sv.load_self()
        except Exception as e:
            SyncLogger.warning(
                "{project_name} | {version} | Failed to load version list!".format(
                    project_name=self.project_name, version=version
                )
            )
            SyncLogger.error("".join(format_exception(e)))
        self.versions.append(sv)

    async def gather_project(self) -> dict:
        return {
            version.version: await version.gather_version() for version in self.versions
        }


class SingleVersion(object):
    def __init__(self, project_id: str, project_name: str, version: str) -> None:
        self.project_id: str = project_id
        self.project_name: str = project_name
        self.version: str = version
        self.builds_list: list = []

    async def load_self(self, retry: int = 0) -> None:
        if retry:
            SyncLogger.warning(
                "{project_id} | {version} | Retrying getting version info..."
            )
        tmp_data = await get_json(
            "https://mohistmc.com/api/v2/projects/{project_id}/{version}/builds".format(
                project_id=self.project_id, version=self.version
            )
        )
        self.builds_list: list = tmp_data.get("builds", None)

        if self.builds_list is None:
            SyncLogger.error(
                "{project_id} | {version} | Failed to get version info!".format(
                    project_id=self.project_id.capitalize(), version=self.version
                )
            )
            return self.load_self(retry=(retry + 1))
        await self.load_builds()

    async def load_builds(self) -> None:
        self.builds = [
            SingleBuild(
                name=self.project_name, version=self.version, build_info=build_info
            )
            for build_info in self.builds_list
        ]

    async def gather_version(self) -> list:
        return [await build.gather_single_build() for build in self.builds]


class SingleBuild(object):
    def __init__(self, name: str, version: str, build_info: dict) -> None:
        self.name = name
        self.version: str = version
        self.build: int = "build" + str(build_info["number"])
        self.time: int = strftime(
            "%Y-%m-%d %H:%M:%S", localtime(int(build_info["createdAt"]) / 1000)
        )
        self.url: str = build_info["url"]

    async def gather_single_build(self) -> dict[str, str]:
        return {
            "sync_time": str(self.time).replace(" ", "T") + "Z",
            "download_url": str(self.url),
            "core_type": self.name,
            "mc_version": str(self.version),
            "core_version": str(self.build),
        }


MohistLoader = _ProjectList
