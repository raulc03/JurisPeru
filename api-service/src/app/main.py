from fastapi import FastAPI
from app.logging_config import setup_logging
from app.api.routes import health, ask

setup_logging()
app = FastAPI(title="02 Project")

app.include_router(router=health.router, prefix="/api")
app.include_router(router=ask.router, prefix="/api")
