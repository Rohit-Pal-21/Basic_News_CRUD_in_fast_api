from fastapi import FastAPI
from app.routers import articles
from .database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(articles.router)
