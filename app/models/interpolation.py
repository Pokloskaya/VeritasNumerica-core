from pydantic import BaseModel

class Interpolation(BaseModel):
    x: list[float]
    y: list[float]