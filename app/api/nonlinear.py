from fastapi import APIRouter, Response, status
import models.nonlinear as NonlinearModels
import services.nonlinear as NonlinearService
from models.response import ResponseModel

router = APIRouter()


def resolve_response(result, table, error, response: Response):
    if error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, error)

    data = {"root": result}

    if table is None:
        return ResponseModel(data, True, None)

    data["columns"] = table["columns"]
    data["rows"] = table["rows"]

    return ResponseModel(data, True, None)


@router.post("/bisection")
def bisection(input_data: NonlinearModels.Bisection, response: Response):
    try:
        result, table, error = NonlinearService.Bisection(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)


@router.post("/fixed_point")
def fixed_point(input_data: NonlinearModels.FixedPoint, response: Response):
    try:
        result, table, error = NonlinearService.Fixed_point(
            input_data.x0, input_data.fx, input_data.gx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)


@router.post("/false_position")
def false_position(input_data: NonlinearModels.FalsePosition, response: Response):
    try:
        result, table, error = NonlinearService.False_position(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)


@router.post("/newton")
def newton(input_data: NonlinearModels.Newton, response: Response):
    try:
        result, table, error = NonlinearService.Newton(
            input_data.x0, input_data.fx, input_data.tol,
            input_data.niter, False, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)


@router.post("/secant")
def secant(input_data: NonlinearModels.Secant, response: Response):
    try:
        result, table, error = NonlinearService.Secant(
            input_data.x0, input_data.x1, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)


@router.post("/multiple_roots")
def multiple_roots(input_data: NonlinearModels.Newton, response: Response):
    try:
        result, table, error = NonlinearService.Newton(
            input_data.x0, input_data.fx, input_data.tol,
            input_data.niter, True, input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(result, table, error, response)
