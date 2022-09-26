import time
from fastapi import APIRouter, Request, Response
from repositories import ClientRepository
import datetime
router = APIRouter()


@router.get("/transactions/")
async def get_client_investments(request: Request):
    # Get query params
    date = request.query_params.get("date", None)
    customer_id = request.query_params.get("customer_id", None)

    if (customer_id == None):
        return Response(status_code=400, content="Missing customer_id")

    avaliable = request.query_params.get("sellout", None)
    if avaliable != None:
        avaliable = avaliable == "true"

    # Get a client and its investments
    return ClientRepository.get_investments(customer_id, date, avaliable)


@router.get("/operations/")
async def get_client_operations(request: Request):
    # Get query params
    date = request.query_params.get(
        "date", datetime.datetime.now().strftime("%Y-%m"))
    customer_id = request.query_params.get("customer_id", None)

    if (customer_id == None):
        return Response(status_code=400, content="Missing customer_id")

    profit_loss = ClientRepository.get_profit_loss(customer_id, date)
    investments = ClientRepository.get_investments(customer_id, date, True)

    return {
        "profit_losses": profit_loss,
        "investments": investments
    }


@router.get("/get_tax/")
async def get_client_tax(request: Request):
    # Get query params
    date = request.query_params.get(
        "date", datetime.datetime.now().strftime("%Y-%m"))
    customer_id = request.query_params.get("customer_id", None)

    if (customer_id == None):
        return Response(status_code=400, content="Missing customer_id")

    # Get a client and its investments
    return ClientRepository.calculate_tax(customer_id, date)
