class ProjectList(object):
    # https://api.papermc.io/v2/projects/
    def __init__(self, data: dict) -> None:
        self.project_list: list = data["projects"]


class Project(object):
    # https://api.papermc.io/v2/projects/{project_name}/
    def __init__(self, data: dict) -> None:
        self.project_id: str = data["project_id"]
        self.project_name: str = data["project_name"]
        self.version_groups: list = data["version_groups"]
        self.versions: list = data["versions"]


class SingleVersion(object):
    # https://api.papermc.io/v2/projects/{name}/versions/{version}/
    def __init__(self, data: dict) -> None:
        self.project_id: str = data["project_id"]
        self.project_name: str = data["project_name"]
        self.version: str = data["version"]
        self.builds: list = data["builds"]


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
