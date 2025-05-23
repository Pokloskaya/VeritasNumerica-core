from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.nonlinear import router as NonlinearRouter
from api.systems import router as SystemsRouter
from api.interpolation import router as InterpolationRouter
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(NonlinearRouter, tags=["Nonlinear"], prefix="/nonlinear")
app.include_router(SystemsRouter, tags=["Systems"], prefix="/systems")
app.include_router(InterpolationRouter, tags=[
                   "Interpolation"], prefix="/interpolation")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to VeritasNumercis API; seeking the true numerical solution"} 

if __name__ == "__main__":
    port = config("PORT", default=8000, cast=int)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
