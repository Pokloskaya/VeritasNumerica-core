from fastapi import APIRouter, Response, status
import models.interpolation as InterpolationModels
import services.interpolation as InterpolationService
from models.response import ResponseModel

router = APIRouter()


@router.post("/vandermonde")
def vandermonde(input_data: InterpolationModels.Interpolation,
                response: Response):
    try:
        v_matrix, b, polynomial, error = InterpolationService.Vandermonde(
            input_data.x, input_data.y
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)
        data = {
            "v_matrix": v_matrix,
            "b": b,
            "polynomial": polynomial
        }
        return ResponseModel(data, True, None)
    except Exception:
        return ResponseModel(None, False, "Invalid input")


@router.post("/newton")
def newton(input_data: InterpolationModels.Interpolation, response: Response):
    try:
        table, polynomial, error = InterpolationService.Newton(
            input_data.x, input_data.y
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)
        data = {
            "rows": table["rows"],
            "columns": table["columns"],
            "polynomial": polynomial
        }
        return ResponseModel(data, True, None)
    except Exception:
        return ResponseModel(None, False, "Invalid input")


@router.post("/lagrange")
def lagrange(input_data: InterpolationModels.Interpolation,
             response: Response):
    try:
        polynomial, texPolynomial, error = InterpolationService.Lagrange(
            input_data.x, input_data.y
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)
        data = {
            "polynomial": polynomial,
            "texPolynomial": texPolynomial
        }
        return ResponseModel(data, True, None)
    except Exception:
        return ResponseModel(None, False, "Invalid input")


@router.post("/linear_spline")
def linear_spline(input_data: InterpolationModels.Interpolation,
                  response: Response):
    try:
        matrix, tracers, error = InterpolationService.LinearSpline(
            input_data.x, input_data.y
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)
        data = {
            "matrix": matrix,
            "tracers": tracers
        }
        return ResponseModel(data, True, None)
    except Exception:
        return ResponseModel(None, False, "Invalid input")


@router.post("/cubic_spline")
def cubic_spline(input_data: InterpolationModels.Interpolation,
                 response: Response):
    try:
        matrix, tracers, error = InterpolationService.CubicSpline(
            input_data.x, input_data.y
        )
        if error:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return ResponseModel(None, False, error)
        data = {
            "matrix": matrix,
            "tracers": tracers
        }
        return ResponseModel(data, True, None)
    except Exception:
        return ResponseModel(None, False, "Invalid input")