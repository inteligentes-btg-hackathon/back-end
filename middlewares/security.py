import time
from fastapi import APIRouter, Request, Response, FastAPI


def setup(app: FastAPI) -> None:
    """Setup the middleware"""
    @app.middleware("http")
    async def remove_server_header(request: Request, call_next):
        """Remove the server header"""
        response = await call_next(request)
        del response.headers["Server"]
        del response.headers["X-Powered-By"]
        return response

    @app.middleware("http")
    async def add_content_type_header(request: Request, call_next):
        """Remove the server header"""
        response = await call_next(request)
        response.headers["content-type"] = "application/pdf"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Content-Disposition"] = f'attachment; filename=darf.pdf'

        return response
