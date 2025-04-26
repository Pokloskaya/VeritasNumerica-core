from fastapi import APIRouter, Response, status
import models.systems as SystemsModels
import services.systems as SystemsService
from models.response import ResponseModel

router = APIRouter()

def resolve_response(data, error, response: Response):
    if error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ResponseModel(None, False, error)

    if data is None:
        return ResponseModel(data, True, None)

    return ResponseModel(data, True, None)

@router.post("/jacobi")
def jacobi(input_data: SystemsModels.Jacobi, response: Response):
    try:
        data, error = SystemsService.Iterative_methods(
            input_data.A, input_data.b, input_data.x0,
            input_data.tol, input_data.niter, "jacobi",
            input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(data, error, response)

@router.post("/gauss-seidel")
def gauss_seidel(input_data: SystemsModels.GaussSeidel, response: Response):
    try:
        data, error = SystemsService.Iterative_methods(
            input_data.A, input_data.b, input_data.x0,
            input_data.tol, input_data.niter, "gauss",
            input_data.relativeError
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(data, error, response)

@router.post("/sor")
def sor(input_data: SystemsModels.SOR, response: Response):
    try:
        data, error = SystemsService.Iterative_methods(
            input_data.A, input_data.b, input_data.x0,
            input_data.tol, input_data.niter, "gauss",
            input_data.relativeError, input_data.w
        )
    except Exception:
        return ResponseModel(None, False, "Invalid input")
    return resolve_response(data, error, response)