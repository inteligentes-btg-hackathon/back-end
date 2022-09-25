import time
from fastapi import APIRouter, Request, Response, FastAPI


def setup(app: FastAPI) -> None:
    """Setup the middleware"""
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
