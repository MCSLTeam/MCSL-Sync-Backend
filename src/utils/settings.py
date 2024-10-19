from orjson import loads, dumps, OPT_INDENT_2
from os import path as osp, makedirs, name as osname, getenv, getlogin
from .logger import SyncLogger
from .database import init_database
from aiohttp import ClientSession
from platform import processor, system as sysType
from hashlib import md5
from random import randint

config_template = {
    "url": "0.0.0.0",
    "port": 4523,
    "ssl_cert_path": "",
    "ssl_key_path": "",
    "node_list": [],
    "secret_key": "".join(
        [
            md5(
                f"{getlogin() if osname == 'nt' else getenv('USER')}{processor()}{sysType()}".encode()
            ).hexdigest()[i : i + 4]
            for i in range(0, 24, 1)
        ]
    ),
}
makedirs("data", exist_ok=True)
makedirs("logs", exist_ok=True)
makedirs("data/runtime", exist_ok=True)


def init_settings() -> None:
    SyncLogger.info("Initializing Settings...")
    if not osp.exists("data/settings.json"):
        with open(
            file="data/settings.json",
            mode="wb+",
        ) as newConfig:
            newConfig.write(dumps(config_template, option=OPT_INDENT_2))
    else:
        pass
    SyncLogger.info("Initializing Database...")
    init_database()


def read_settings() -> dict:
    try:
        with open(file="data/settings.json", mode="r", encoding="utf-8") as f:
            cfg = loads(f.read())
        return cfg
    except FileNotFoundError:
        init_settings()
        read_settings()


cfg = read_settings()


def add_node(node: str) -> None:
    cfg = read_settings()
    pre_data = {
        "type": node.split("|")[0],
        "endpoint": node.split("|")[1],
        "name": node.split("|")[2],
    }
    if pre_data.get("type").startswith("alist"):
        pre_data["alist_subpath"] = pre_data["type"].split("@")[1]
        pre_data["type"] = "alist"
    cfg["node_list"].append(pre_data)
    with open(file="data/settings.json", mode="w", encoding="utf-8") as f:
        f.write(dumps(cfg, option=OPT_INDENT_2))


async def is_node_available(node: str) -> bool:
    try:
        async with ClientSession() as session:
            async with session.get(node) as response:
                return response.status == 200
    except Exception:
        return False


async def get_available_node() -> dict:
    cfg = read_settings()
    # available_nodes = []
    # for node in cfg["node_list"]:
    #     # if await is_node_available(node):
    #     available_nodes.append(node)
    available_nodes = cfg["node_list"]
    if len(available_nodes):
        return available_nodes[
            randint(0, len(available_nodes) - 1) if len(available_nodes) > 1 else 0
        ]
    else:
        return "error"
