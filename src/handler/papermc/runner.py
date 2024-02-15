from .base import PaperLoader


async def papermc_runner() -> None:
    project_list = PaperLoader()
    await project_list.load_self()
    await project_list.load_all_projects()
