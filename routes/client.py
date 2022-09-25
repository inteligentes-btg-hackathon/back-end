import time
from fastapi import APIRouter, Request, Response
from services import ClientService
router = APIRouter()


@router.get("/clients")
async def get_clients(request: Request):
    # Get all clients
    return ClientService.get_all()
