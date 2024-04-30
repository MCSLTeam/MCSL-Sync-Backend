from orjson import loads, dumps, OPT_INDENT_2
from os import path as osp, makedirs, name as osname, getenv, getlogin
from .logger import SyncLogger
from .database import init_pre_database, init_production_database
from platform import processor, system as sysType
from hashlib import md5

config_template = {
    "url": "0.0.0.0",
    "port": 4523,
    "ssl_cert_path": "",
    "ssl_key_path": "",
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
makedirs("data/production", exist_ok=True)
makedirs("data/runtime", exist_ok=True)


def init_settings() -> None:
    SyncLogger.info("Initialize Settings...")
    if not osp.exists("data/settings.json"):
        with open(
            file="data/settings.json",
            mode="wb+",
        ) as newConfig:
            newConfig.write(dumps(config_template, option=OPT_INDENT_2))
    else:
        pass
    SyncLogger.info("Initialize Runtime Temporary TempoDatabase...")
    init_pre_database()

    SyncLogger.info("Initialize Production Database...")
    init_production_database()


def read_settings() -> dict:
    with open(file="data/settings.json", mode="r", encoding="utf-8") as f:
        cfg = loads(f.read())
    return cfg


cfg = read_settings()  # type: dict
