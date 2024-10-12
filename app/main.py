from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.routers import items, clock_in

app = FastAPI()

# Include routers
app.include_router(items.router, tags=["items"])
app.include_router(clock_in.router, tags=["clock-in"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI CRUD application!"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
