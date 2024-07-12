from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.router import router
app = FastAPI(default_response_class=ORJSONResponse)
app.include_router(router)