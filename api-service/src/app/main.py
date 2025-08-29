from fastapi import FastAPI
from app.logging_config import setup_logging
from app.api.routes import health, ask
from fastapi.middleware.cors import CORSMiddleware


setup_logging()
app = FastAPI(title="API Law Services")  # TODO: lifespan: warmup the embedding model

origins = ["http://localhost:8501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router=health.router, prefix="/api")
app.include_router(router=ask.router, prefix="/api")
