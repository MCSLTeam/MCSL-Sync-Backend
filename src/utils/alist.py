import aiohttp
import json

async def get_alist_file_url(host: str, path: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{host}api/fs/get?path={path}") as response:
            if response.status != 200:
                return None
            response_data = await response.text()
            remote_file_detail = json.loads(response_data).get("data")
            if remote_file_detail:
                return remote_file_detail.get("raw_url")
            return None