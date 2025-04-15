from pydantic import BaseModel


class Bisection(BaseModel):
    a: str
    b: str
    tol: float
    fx: str
    niter: int
    relativeError: bool


class FixedPoint(BaseModel):
    x0: str
    fx: str
    gx: str
    tol: float
    niter: int
    relativeError: bool


class FalsePosition(BaseModel):
    a: str
    b: str
    fx: str
    tol: float
    niter: int
    relativeError: bool


class Newton(BaseModel):
    x0: str
    fx: str
    tol: float
    niter: int
    relativeError: bool


class Secant(BaseModel):
    x0: str
    x1: str
    fx: str
    tol: float
    niter: int
    relativeError: bool
