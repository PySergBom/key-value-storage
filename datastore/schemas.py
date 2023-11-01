from pydantic import BaseModel


class SetValueRequest(BaseModel):
    key: str
    value: str


class DeleteValueRequest(BaseModel):
    key: str