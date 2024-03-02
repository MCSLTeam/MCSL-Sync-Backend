from fastapi import status
from fastapi.responses import ORJSONResponse, Response
from typing import Union


def gen_response(
    *,
    status_code=status.HTTP_200_OK,
    data: Union[list, dict, str] = None,
    msg: str = "Ok",
) -> Response:
    return ORJSONResponse(
        status_code=status_code,
        content={
            "data": data,
            "code": status_code,
            "msg": msg,
        },
    )
