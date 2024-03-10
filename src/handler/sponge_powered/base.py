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
            SyncLogger.warning("SpongePowered | Retrying getting project list...")
        self.project_id_list = (await get_json("https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts")).get("artifactIds", None)  # noqa: E501
        if self.project_id_list is None:
            SyncLogger.error("SpongePowered | Project list load failed!")
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
        self.project_name: str = ""
        self.version_label_list: list = []
        self.versions: list[SingleVersion] = []

    async def load_self(self, retry: int = 0) -> None:
        if retry:
            SyncLogger.warning(
                "{project_id} | Retrying getting project info..."
            )
        tmp_data = await get_json(
            "https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts/{project_id}".format(
                project_id=self.project_id
            )
        )  # type: dict

        self.project_name = tmp_data.get("displayName", None)
        self.version_label_list = tmp_data["tags"]["minecraft"]

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
        self.build_label_list: list = []
        self.builds_manager: BuildsManager | None = None

    async def load_self(self, retry: int = 0) -> None:
        if retry:
            SyncLogger.warning(
                "{project_id} | {version} | Retrying getting version info..."
            )
        self.build_label_list = list(
            dict(
                await get_json(
                    "https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts/{project_id}/versions?tags=,minecraft:{version}&offset=0&limit=10".format(
                        project_id=self.project_id, version=self.version
                    )
                )
            ).get("artifacts", None)
        )
        if self.build_label_list == [None]:
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
            build_label_list=self.build_label_list,
        )
        await self.load_builds()

    async def load_builds(self) -> None:
        await create_task(self.builds_manager.load_self())

    async def gather_version(self) -> list:
        return await self.builds_manager.gather_builds()


class BuildsManager(object):
    def __init__(
        self, project_name: str, project_id: str, version: str, build_label_list: list
    ) -> None:
        self.project_name: str = project_name
        self.project_id: str = project_id
        self.version: str = version
        self.build_label_list: list = build_label_list
        self.builds: list = []

    async def load_self(self) -> None:
        self.builds = [
            await get_json(
                "https://dl-api.spongepowered.org/v2/groups/org.spongepowered/artifacts/{project_id}/versions/{build_label}".format(
                    project_id=self.project_id, build_label=build_label
                )
            )
            for build_label in self.build_label_list
        ]

    async def get_universal_build(self, build_assets: list) -> str:
        if build_assets is None:
            SyncLogger.warning(
                "Fuck you SpongePowered! You didn't synchronized your motherfuckers old API!"
            )
            return None
        else:
            try:
                return [
                    asset["downloadUrl"]
                    for asset in build_assets
                    if asset["classifier"] == "universal"
                ][0]
            except IndexError:
                try:
                    return [
                        asset["downloadUrl"]
                        for asset in build_assets
                        if (not asset["classifier"] and asset["extension"] != "pom")
                    ][0]
                except IndexError:
                    SyncLogger.warning(
                        "Fuck you SpongePowered! You didn't built anything for this version!"
                    )
                    return None

    async def gather_builds(self) -> list:
        tmp_list = []
        for build_info in self.builds:
            if (
                await self.get_universal_build(build_info.get("assets", None))
                is not None
            ):
                tmp_list.append(
                    {
                        "sync_time": "1970-01-01T00:00:00Z",
                        "download_url": await self.get_universal_build(
                            build_info.get("assets", None)
                        ),
                        "core_type": self.project_name,
                        "mc_version": str(self.version),
                        "core_version": (
                            str(
                                build_info.get("coordinates", {})
                                .get("version", "")
                                .replace(str(self.version + "-"), "")
                            )
                            if build_info.get("coordinates", None) is not None
                            else None
                        ),
                    }
                )
            else:
                continue
        return tmp_list


SpongePoweredLoader = _ProjectList
