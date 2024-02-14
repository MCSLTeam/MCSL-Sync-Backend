import asyncio
from src.handler.papermc.base import PaperLoader


async def main() -> None:
    project_list = PaperLoader()
    await project_list.load_self()
    await project_list.load_all_projects()

asyncio.run(main())
