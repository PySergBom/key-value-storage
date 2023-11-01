from fastapi import APIRouter, Request, HTTPException

from api.transactions.transaction_manager import transaction_manager

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("/begin/")
def begin_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Неоходима авторизация")
    transaction_manager.begin_transaction()
    transaction_manager.transaction_initiator = user
    return {"message": "Открыта транзакция"}


@router.post("/rollback/")
def rollback_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Неоходима авторизация")
    try:
        transaction_manager.rollback_transaction()
        return {"message": "Последняя транзакция отменена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/commit/")
def commit_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Неоходима авторизация")
    try:
        transaction_manager.commit_transaction()
        return "Сommit complete"
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
