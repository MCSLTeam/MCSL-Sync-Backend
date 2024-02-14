from ...utils import get_json, SyncLogger


class _ProjectList(object):
    def __init__(self) -> None:
        self.project_id_list: list = []
        self.project_list: list = []

    async def load_self(self) -> None:
        # fmt: off
        SyncLogger.info("PaperMC | Loading project list...")
        self.project_id_list = (await get_json("https://api.papermc.io/v2/projects/"))["projects"]  # noqa: E501
        SyncLogger.success("PaperMC | Project list loaded.")
        SyncLogger.debug("PaperMC | Project list: {project_id_list}".format(project_id_list=self.project_id_list))
        # fmt: on

    async def load_all_projects(self) -> None:
        SyncLogger.info("PaperMC | Loading projects...")
        for project_id in self.project_id_list:
            await self.load_single_project(project_id=project_id)
        SyncLogger.success("PaperMC | All projects were loaded.")

    async def load_single_project(self, project_id: str) -> None:
        SyncLogger.debug("PaperMC | Loading project: \"{project_id}\"".format(project_id=project_id))
        self.project_list.append((p := Project(project_id=project_id)))
        await p.load_self()
        SyncLogger.info("PaperMC | Project \"{project_id}\" loaded.".format(project_id=project_id))


class Project(object):
    def __init__(self, project_id: str) -> None:
        self.project_id: str = project_id
        self.project_name: str = []
        self.version_groups: list = []
        self.versions: list = []

    async def load_self(self) -> None:
        tmp_data = await get_json(
            "https://api.papermc.io/v2/projects/{project_id}/".format(
                project_id=self.project_id
            )
        )

        self.project_name: str = tmp_data["project_name"]
        self.version_groups: list = tmp_data["version_groups"]
        self.versions: list = tmp_data["versions"]


class SingleVersion(object):
    # https://api.papermc.io/v2/projects/{project_id}/versions/{version}/
    def __init__(self, data: dict) -> None:
        self.project_id: str = data["project_id"]
        self.project_name: str = data["project_name"]
        self.version: str = data["version"]
        self.builds_number: list = data["builds"]
        self.builds: list = []


class SingleChange(object):
    def __init__(self, data: dict) -> None:
        self.commit: str = data["commit"]
        self.summary: str = data["summary"]
        self.message: str = data["message"]


class Changes(object):
    def __init__(self, data: dict) -> None:
        self.changes: list = [SingleChange(data) for data in data["changes"]]


class SingleDownload(object):
    def __init__(self, data: dict, name: str, version: str, build: int) -> None:
        self.name: str = data["name"]
        self.link: str = "https://api.papermc.io/v2/projects/{name}/versions/{version}/builds/{build}/downloads/{file_name}/".format(
            name=name, version=version, build=build, file_name=self.name
        )
        self.sha256: str = data["sha256"]

    def __str__(self) -> str:
        return self.link


class Downloads(object):
    def __init__(self, data: dict, name: str, version: str, build: int) -> None:
        self.application: SingleDownload = SingleDownload(
            data=data["application"], name=name, version=version, build=build
        )
        self.mojmap: SingleDownload = SingleDownload(
            data=data["mojang-mappings"], name=name, version=version, build=build
        )


class SingleBuild(object):
    def __init__(self, data: dict) -> None:
        self.build: int = data["build"]
        self.time: int = data["time"]
        self.channel: int = data["channel"]
        self.promoted: int = data["promoted"]
        self.changes: Changes = Changes(data["changes"])
        self.downloads: dict[str, Downloads] = {
            "application": Downloads(data["downloads"]["application"]),
            "mojang-mappings": Downloads(data["downloads"]["mojang-mappings"]),
        }


class Builds(object):
    # https://api.papermc.io/v2/projects/{name}/versions/{version}/builds/
    def __init__(self, data: dict) -> None:
        self.project_id: str = data["project_id"]
        self.project_name: str = data["project_name"]
        self.version: str = data["version"]
        self.builds: list[SingleBuild] = [SingleBuild(data) for data in data["builds"]]

PaperLoader = _ProjectList