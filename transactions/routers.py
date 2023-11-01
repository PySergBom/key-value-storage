from fastapi import APIRouter, HTTPException, Request

from transactions.transaction_manager import transaction_manager

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
    return {"message": "Transaction opened"}


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
        return {"message": "Last transaction canceled"}
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
            detail="Authorization is required"
        )
    if transaction_stack:
        if transaction_initiator != user:
            raise HTTPException(
                status_code=400,
                detail="The data is read-only. Transaction opened"
            )
