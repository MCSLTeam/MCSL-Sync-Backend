from quart import Quart, make_response
from quart_cors import cors, route_cors
from typing import Union
from orjson import dumps

app = Quart(__name__)
app = cors(app, allow_origin="*")  # 允许所有源


async def gen_response(
    *,
    status_code=200,
    data: Union[list, dict, str] = None,
    msg: str = "Ok",
):
    response = await make_response(
        dumps(
            {
                "data": data,
                "code": status_code,
                "msg": msg,
            },
        ),
        status_code,
    )
    response = route_cors(response, allow_origin="*")  # 允许所有源
    response.mimetype = "application/json"
    return response
