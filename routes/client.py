import time
from fastapi import APIRouter, Request, Response
from services import Client
router = APIRouter()


@router.get("/clients")
async def get_clients(request: Request):
    # Get all clients
    return Client.get_all()
