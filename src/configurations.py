from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


class CORS:
    def setup(app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
