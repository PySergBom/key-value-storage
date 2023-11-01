from fastapi import APIRouter, HTTPException, Request

from api.datastore.datastore import data_store
from api.datastore.schemas import DeleteValueRequest, SetValueRequest
from api.transactions.transaction_manager import transaction_manager

router = APIRouter(
    prefix="/kvs",
    tags=["Key Value Store"],
)


@router.post("/set_value/")
def set_value(request: SetValueRequest, request_cookies: Request):
    key, value = request.key, request.value
    if transaction_manager.stack:
        if transaction_manager.initiator != request_cookies.cookies.get("user"):
            raise HTTPException(
                status_code=400,
                detail="Данные доступны только для чтения. Открыта транзакция"
            )
        transaction_manager.current_transaction[key] = value
        return {"message": "Значение задано в транзакции"}
    try:
        data_store.set_value(key, value)
        return {"message": "Значение сохранено"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_value/")
def get_value(key: str):
    value = data_store.get_value(key)
    if value is not None:
        return {"value": value}
    raise HTTPException(status_code=404, detail="Ключ не найден")


@router.delete("/delete_value/")
def delete_value(request: DeleteValueRequest):
    key = request.key
    if transaction_manager.stack:
        raise HTTPException(
            status_code=400,
            detail="Открыта транзакция. Удаление не возможно"
        )
    try:
        data_store.delete_value(key)
        return {"message": "Значение удалено"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/find_keys")
def find_keys(value: str):
    keys = data_store.find_keys(value)
    return {"keys": keys}
