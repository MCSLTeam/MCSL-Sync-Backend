from ...utils import get_json, SyncLogger, update_database
from traceback import format_exception
from asyncio import create_task


class _ProjectList(object):
    def __init__(self) -> None:
        self.project_id_list: list = []
        self.project_list: list = []

    async def load_self(self, retry: int = 0) -> None:
        # fmt: off
        if retry:
            SyncLogger.warning("PaperMC | Retrying getting project list...")
        self.project_id_list = (await get_json("https://api.papermc.io/v2/projects/")).get("projects", None)  # noqa: E501
        if self.project_id_list is None:
            SyncLogger.error("PaperMC | Project list load failed!")
            return self.load_self(retry=(retry+1))
        # fmt: on

    async def load_all_projects(self) -> None:
        tasks = [
            create_task(self.load_single_project(project_id=project_id))
            for project_id in self.project_id_list
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
            SyncLogger.warning(f"{self.project_name} | Retrying getting project info...")
        tmp_data = await get_json(
            "https://api.papermc.io/v2/projects/{project_id}/".format(
                project_id=self.project_id
            )
        )  # type: dict

        self.project_name = tmp_data.get("project_name", None)
        self.version_label_list = tmp_data.get("versions", None)

        if self.project_name is None or self.version_label_list is None:
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
        self.builds_number: list = []
        self.builds_manager: BuildsManager | None = None

    async def load_self(self, retry: int = 0) -> None:
        if retry:
            SyncLogger.warning(
                "{project_id} | {version} | Retrying getting version info..."
            )
        tmp_data = await get_json(
            "https://api.papermc.io/v2/projects/{project_id}/versions/{version}/".format(
                project_id=self.project_id, version=self.version
            )
        )
        self.builds_number: list = tmp_data.get("builds", None)

        if self.builds_number is None:
            SyncLogger.error(
                "{project_id} | {version} | Failed to get version info!".format(
                    project_id=self.project_id.capitalize(), version=self.version
                )
            )
            return self.load_self(retry=(retry + 1))

        self.builds_manager = BuildsManager(
            project_name=self.project_name,
            project_id=self.project_id,
            version=self.version,
        )
        await self.load_builds()

    async def load_builds(self) -> None:
        await create_task(self.builds_manager.load_self())

    async def gather_version(self) -> list:
        return await self.builds_manager.gather_builds()


class SingleDownload(object):
    def __init__(self, data: dict, name: str, version: str, build: int) -> None:
        if data is None:
            self.name = None
            self.sha256 = None
        else:
            self.name: str = data.get("name", None)
            self.sha256: str = data.get("sha256", None)
        self.link: str = "https://api.papermc.io/v2/projects/{name}/versions/{version}/builds/{build}/downloads/{file_name}".format(
            name=name.lower(), version=version, build=build, file_name=self.name
        )

    def __str__(self) -> str:
        return self.link


class Downloads(object):
    def __init__(self, data: dict, name: str, version: str, build: int) -> None:
        self.application: SingleDownload = SingleDownload(
            data=data.get("application", None), name=name, version=version, build=build
        )

    def __str__(self) -> str:
        return self.application.link


class SingleBuild(object):
    def __init__(self, name: str, version: str, build_info: dict) -> None:
        self.name = name
        self.version: str = version
        self.build: int = build_info["build"]
        self.time: str = build_info["time"]
        self.downloads: Downloads = Downloads(
            data=build_info["downloads"], name=name, version=version, build=self.build
        )

    async def gather_single_build(self) -> dict[str, str]:
        return {
            "sync_time": str(self.time).split(".")[0] + "Z",
            "download_url": str(self.downloads),
            "core_type": self.name,
            "mc_version": str(self.version),
            "core_version": "build" + str(self.build),
        }


class BuildsManager(object):
    def __init__(self, project_name: str, project_id: str, version: str) -> None:
        self.project_name: str = project_name
        self.project_id: str = project_id
        self.version: str = version
        self.builds: list[SingleBuild] = []

    async def load_self(self) -> None:
        try:
            tmp_data = await get_json(
                "https://api.papermc.io/v2/projects/{project_id}/versions/{version}/builds/".format(
                    project_id=self.project_id, version=self.version
                )
            )
            self.builds = [
                SingleBuild(
                    name=self.project_name, version=self.version, build_info=build_info
                )
                for build_info in tmp_data.get("builds", None)
            ]
        except Exception as e:
            SyncLogger.warning(
                "{project_name} | {version} | Failed to load builds!".format(
                    project_name=self.project_name,
                    version=self.version,
                )
            )
            SyncLogger.error("".join(format_exception(e)))

    async def gather_builds(self) -> list:
        return [await build.gather_single_build() for build in self.builds]


PaperLoader = _ProjectList
