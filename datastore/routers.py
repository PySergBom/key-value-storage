from fastapi import APIRouter, HTTPException, Request

from datastore.datastore import data_store
from datastore.schemas import DeleteValueRequest, SetValueRequest
from transactions.transaction_manager import transaction_manager

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
                detail="The data is read-only. Transaction opened"
            )
        transaction_manager.current_transaction[key] = value
        return {"message": "The value is set in the transaction"}
    try:
        data_store.set_value(key, value)
        return {"message": "The value is saved"}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_value/")
def get_value(key: str):
    value = data_store.get_value(key)
    if value is not None:
        return {"value": value}
    raise HTTPException(status_code=404, detail="Key not found")


@router.delete("/delete_value/")
def delete_value(request: DeleteValueRequest):
    key = request.key
    if transaction_manager.stack:
        raise HTTPException(
            status_code=400,
            detail="A transaction has been opened. Deletion is not possible"
        )
    try:
        data_store.delete_value(key)
        return {"message": "Value removed"}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/find_keys")
def find_keys(value: str):
    keys = data_store.find_keys(value)
    return {"keys": keys}
