from aiohttp import ClientSession
from .logger import __version__
from .logger import SyncLogger


@SyncLogger.catch
async def get_proxy() -> str | None:
    from urllib.request import getproxies

    try:
        proxy = getproxies()["http"]
    except KeyError:
        proxy = None
    del getproxies
    return proxy


@SyncLogger.catch
async def get_json(link: str) -> dict | list | None:
    trust_env = not bool(isinstance(await get_proxy(), str))
    async with ClientSession(
        trust_env=trust_env,
        headers={
            "User-Agent": f"MCSLSync/{__version__} Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ) as session:
        async with session.get(link) as response:
            return await response.json()


@SyncLogger.catch
async def get_text(link: str) -> str | None:
    trust_env = not bool(isinstance(await get_proxy(), str))
    async with ClientSession(
        trust_env=trust_env,
        headers={
            "User-Agent": f"MCSLSync/{__version__} Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
    ) as session:
        async with session.get(link) as response:
            return await response.text()
