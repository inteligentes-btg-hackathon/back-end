import time
from fastapi import APIRouter, Request, Response
from database import db, QueryConstructor

router = APIRouter()


@router.get("/clients")
async def get_clients(request: Request):
    # Get all clients
    query = QueryConstructor('clients')
    query.select()
    query.inner_join('banks', 'banks.id', 'any(clients.banks_ids)')
    query.execute()
    return query.result
