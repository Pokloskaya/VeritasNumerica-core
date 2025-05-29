from fastapi import APIRouter, Response, status
import models.interpolation as InterpolationModels
import services.interpolation as InterpolationService
from models.response import ResponseModel
from models.interpolation import Interpolation

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

@router.post("/compare_all")
def compare_all(input_data: Interpolation, response: Response):
    results = []

    methods = [
        ("vandermonde", lambda: InterpolationService.Vandermonde(input_data.x, input_data.y)),
        ("newton", lambda: InterpolationService.Newton(input_data.x, input_data.y)),
        ("lagrange", lambda: InterpolationService.Lagrange(input_data.x, input_data.y)),
        ("linear_spline", lambda: InterpolationService.LinearSpline(input_data.x, input_data.y)),
        ("cubic_spline", lambda: InterpolationService.CubicSpline(input_data.x, input_data.y)),
    ]

    for name, method in methods:
        try:
            result = method()
            success = result[-1] is None
            output = {
                "method": name,
                "success": success,
                "error_msg": result[-1] if not success else None
            }

            if name == "vandermonde":
                output.update({
                    "matrix": result[0],
                    "b": result[1],
                    "polynomial": result[2]
                })
            elif name == "newton":
                output.update({
                    "table": result[0],
                    "polynomial": result[1]
                })
            elif name == "lagrange":
                output.update({
                    "polynomial": result[0],
                    "tex_polynomial": result[1]
                })
            elif name == "linear_spline":
                output.update({
                    "matrix": result[0],
                    "tracers": result[1]
                })
            elif name == "cubic_spline":
                output.update({
                    "matrix": result[0],
                    "tracers": result[1]
                })

            results.append(output)

        except Exception as e:
            results.append({
                "method": name,
                "success": False,
                "error_msg": str(e)
            })

    successful = [r for r in results if r["success"]]

    best = None
    if successful:
        best = min(successful, key=lambda r: len(r.get("matrix", r.get("polynomial", ""))))

    # Aquí está el cambio: retornamos como el frontend espera
    return {
        "success": True,
        "data": {
            "methods": {r["method"]: r for r in results},
            "best": {
                "method": best["method"],
                "polynomial": best.get("polynomial", "")
            } if best else None
        }
    }
