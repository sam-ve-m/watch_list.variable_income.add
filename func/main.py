# Jormungandr
from src.domain.enums.response.code import InternalCode
from src.domain.exceptions import UnauthorizedError
from src.domain.validator import WatchListSymbols
from src.services.watch_list import WatchListService
from src.domain.response.model import ResponseModel
from heimdall_client.bifrost import Heimdall

# Standards
from http import HTTPStatus

# Third party
from flask import request,Request
from etria_logger import Gladsheim


async def save_symbols(request: Request = request):
    raw_params = request.json
    x_thebes_answer = request.headers.get('x-thebes-answer')

    try:
        jwt_content, heimdall_status = await Heimdall.decode_payload(jwt=x_thebes_answer)
        if not jwt_content["is_payload_decoded"]:
            raise UnauthorizedError()

        watch_list_symbols = WatchListSymbols(**raw_params)
        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        result = await WatchListService.register(watch_list_symbols=watch_list_symbols, unique_id=unique_id)

        response = ResponseModel(
            success=result,
            code=InternalCode.SUCCESS,
            message="Symbols successfully saved",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError:
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UnauthorizedError:
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="JWT invalid or not supplied."
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
