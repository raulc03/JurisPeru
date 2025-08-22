from fastapi import FastAPI
from app.logging_config import setup_logging
from app.api.routes import health

setup_logging()
app = FastAPI(title="02 Project")

app.include_router(prefix="/api", router=health.router)
