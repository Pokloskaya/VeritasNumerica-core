from pydantic import BaseModel

class Jacobi(BaseModel):
    A: list
    b: list
    x0: list
    tol: float
    niter: int
    relativeError: bool

class GaussSeidel(BaseModel):
    A: list
    b: list
    x0: list
    tol: float
    niter: int
    relativeError: bool

class SOR(BaseModel):
    A: list
    b: list
    x0: list
    w: float
    tol: float
    niter: int
    relativeError: bool