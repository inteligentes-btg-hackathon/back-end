import time
from fastapi import APIRouter, Request, Response
from repositories import DarfRepository

router = APIRouter()


@router.get("/darf")
def generate_darf(request: Request):
    customer_id = request.query_params.get("customer_id", None)
    date = request.query_params.get("date", None)

    if customer_id is None:
        return {
            "error": "customer_id is required"
        }

    if date is None:
        return {
            "error": "date is required"
        }

    return DarfRepository.generate_darf(customer_id, date)


@router.post("/check_payment")
def check_payment(request: Request):
    customer_id = request.query_params.get("customer_id", None)
    date = request.query_params.get("date", None)

    if customer_id is None:
        return {
            "error": "customer_id is required"
        }

    if date is None:
        return {
            "error": "date is required"
        }

    return DarfRepository.check_payment(customer_id, date)
