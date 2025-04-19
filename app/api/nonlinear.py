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

@router.post("/compare_all")
def compare_all(input_data: NonlinearModels.CompareAll, response: Response):
    results = []
    methods = [
        ("bisection", lambda: NonlinearService.Bisection(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )),
        ("false_position", lambda: NonlinearService.False_position(
            input_data.a, input_data.b, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )),
        ("fixed_point", lambda: NonlinearService.Fixed_point(
            input_data.x0, input_data.fx, input_data.gx,
            input_data.tol, input_data.niter, input_data.relativeError
        )),
        ("newton", lambda: NonlinearService.Newton(
            input_data.x0, input_data.fx,
            input_data.tol, input_data.niter, False,
            input_data.relativeError
        )),
        ("secant", lambda: NonlinearService.Secant(
            input_data.x0, input_data.x1, input_data.fx,
            input_data.tol, input_data.niter, input_data.relativeError
        )),
        ("multiple_roots", lambda: NonlinearService.Newton(
            input_data.x0, input_data.fx,
            input_data.tol, input_data.niter, True,
            input_data.relativeError
        )),
    ]

    for name, method in methods:
        try:
            root, table, error = method()
            results.append({
                "method": name,
                "success": error is None,
                "root": root,
                "iterations": len(table["rows"]) - 1 if table else None,
                "final_error": table["rows"][-1][-1] if table else None,
                "rows": table["rows"] if table else [],
                "columns": table["columns"] if table else [],
                "error_msg": error
            })
        except Exception as e:
            results.append({
                "method": name,
                "success": False,
                "error_msg": str(e)
            })

    successful = [r for r in results if r["success"]]
    best = None
    if successful:
        best = min(successful, key=lambda r: (r["iterations"], r["final_error"]))

    return {
        "success": True,
        "results": results,
        "best_method": best["method"] if best else None,
        "best_root": best["root"] if best else None,
    }

