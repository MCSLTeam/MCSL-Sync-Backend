
from quart import Quart, request
from werkzeug.exceptions import HTTPException
from ..utils import __version__, cfg

import uvicorn
from .model import gen_response

sync_api = Quart(__name__)

def start_production_server():
    uvicorn.run(
        app=sync_api,
        host=cfg.get("url"),
        port=cfg.get("port"),
        ssl_certfile=cfg.get("ssl_cert_path")
        if cfg.get("ssl_cert_path") != ""
        else None,
        ssl_keyfile=cfg.get("ssl_key_path") if cfg.get("ssl_key_path") != "" else None,
    )

@sync_api.errorhandler(Exception)
async def exception_handler(exc):
    status_code = 500
    if isinstance(exc, HTTPException):
        status_code = exc.code
    return await gen_response(
        data={
            "request": {
                "method": request.method,
                "path": request.path,
            },
            "exception": str(exc),
        },
        status_code=status_code,
        msg=str(exc),
    )

@sync_api.route("/")
async def base_dir():
    """
    This is using docstrings for specifications.
    ---
    parameters:
        none
    responses:
      200:
        description: Say hello to the user
    """
    return await gen_response(
        status_code=200,
        msg=f"MCSL-Sync v{__version__} on Quart!",
    )

@sync_api.route("/public/statistics")
async def get_app_info():
    return await gen_response(
        data={
            "name": "MCSL-Sync",
            "author": "MCSLTeam",
            "version": f"v{__version__}",
            "config": cfg,
        },
        status_code=200,
        msg="Success!",
    )

@sync_api.route("/public/availables")
async def get_available_core_list():
    from ..utils import available_downloads
    resp = await gen_response(
        data=available_downloads,
        status_code=200,
        msg="Success!",
    )
    del available_downloads
    return resp