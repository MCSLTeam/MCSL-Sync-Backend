from fastapi import FastAPI, status
from enum import Enum
import uvicorn
from .model import gen_response
from ..utils import __version__, cfg

sync_api = FastAPI()


def start_api_server():
    uvicorn.run(
        app=sync_api,
        host=cfg.get("url"),
        port=cfg.get("port"),
        ssl_certfile=cfg.get("ssl_cert_path")
        if cfg.get("ssl_cert_path") != ""
        else None,
        ssl_keyfile=cfg.get("ssl_key_path") if cfg.get("ssl_key_path") != "" else None,
    )


# class RouterBase(Enum):
#     def apiPath(self):
#         return f"{self.__path__}{self.value}"


# class APIRouter(RouterBase):
#     __path__ = "/public"


@sync_api.get("/")
def base_dir():
    return gen_response(
        status_code=status.HTTP_200_OK,
        msg=f"MCSL-Sync v{__version__} on FastAPI!",
    )


@sync_api.get("/public/statistics")
def get_app_info():
    return gen_response(
        data={
            "name": "MCSL-Sync",
            "author": "MCSLTeam",
            "version": f"v{__version__}",
            "config": cfg,
        },
        status_code=status.HTTP_200_OK,
        msg="Success!",
    )


@sync_api.get("/public/availables")
def get_available_core_list():
    from ..utils import available_downloads

    resp = gen_response(
        data=available_downloads,
        status_code=status.HTTP_200_OK,
        msg="Success!",
    )
    del available_downloads
    return resp
