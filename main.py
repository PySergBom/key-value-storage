import uvicorn
from fastapi import FastAPI

from api.datastore.routers import router as dr
from api.transactions.routers import router as tr
from api.users.routers import router as ur

app = FastAPI()

app.include_router(ur)
app.include_router(dr)
app.include_router(tr)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
