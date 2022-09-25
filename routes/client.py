import time
import datetime

from fastapi import APIRouter, Request, Response
from repositories import ClientRepository
router = APIRouter()


@router.get("/clients")
async def get_clients(request: Request):
    # Get all clients
    return ClientService.get_all()


@router.get("/clients/{customerId}")
async def get_client_investments(customerId: str, request: Request):
    # Get query params
    date = request.query_params.get("date", None)

    # Get a client and its investments
    return ClientService.get_avaliable_investments(customerId, date)
