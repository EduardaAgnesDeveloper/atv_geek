from fastapi import FastAPI
from controllers_geek import router
from database import sync_database, get_engine

app = FastAPI()
sync_database(get_engine())
app.include_router(router, prefix="/api")