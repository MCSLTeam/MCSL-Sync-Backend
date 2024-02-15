from orjson import loads, dumps
from os import path as osp, makedirs
from .logger import SyncLogger

SyncLogger.info("Reading settings...")
config_template = {"force_fast_loading": False, "debug": True}
cfg = config_template.copy()
makedirs("data", exist_ok=True)
makedirs("logs", exist_ok=True)


if not osp.exists("data/settings.json"):
    with open(
        file="data/settings.json",
        mode="w+",
        encoding="utf-8",
    ) as newConfig:
        newConfig.write(dumps(config_template).decode("utf-8"))
else:
    pass
with open(file="data/settings.json", mode="r", encoding="utf-8") as f:
    cfg = loads(f.read())
