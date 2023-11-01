from fastapi import APIRouter, HTTPException, Request

from api.transactions.transaction_manager import transaction_manager

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post("/begin/")
def begin_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    checking(
        user,
        transaction_manager.stack,
        transaction_manager.initiator
    )
    transaction_manager.begin()
    transaction_manager.initiator = user
    return {"message": "Открыта транзакция"}


@router.post("/rollback/")
def rollback_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    checking(
        user,
        transaction_manager.stack,
        transaction_manager.initiator
    )
    try:
        transaction_manager.rollback()
        return {"message": "Последняя транзакция отменена"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/commit/")
def commit_transaction(request_cookies: Request):
    user = request_cookies.cookies.get("user")
    checking(
        user,
        transaction_manager.stack,
        transaction_manager.initiator
    )
    try:
        transaction_manager.commit()
        return "Commit complete"
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def checking(user, transaction_stack, transaction_initiator):
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неоходима авторизация"
        )
    if transaction_stack:
        if transaction_initiator != user:
            raise HTTPException(
                status_code=400,
                detail="Данные доступны только для чтения. Открыта транзакция"
            )
