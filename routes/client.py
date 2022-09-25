import time
import datetime

from fastapi import APIRouter, Request, Response
from repositories import ClientRepository
router = APIRouter()


@router.get("/clients")
async def get_clients(request: Request):
    # Get all clients
    return ClientRepository.get_all()
