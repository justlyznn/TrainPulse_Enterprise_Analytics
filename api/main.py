from fastapi import FastAPI
from .database import engine
from . import models
from .routers import participants, sessions, analytics, predict

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrainPulse API",
    description="API for TrainPulse: Employee Training Analytics and Prediction Platform",
    version="1.0.0"
)

app.include_router(participants.router)
app.include_router(sessions.router)
app.include_router(analytics.router)
app.include_router(predict.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TrainPulse API. Visit /docs for API documentation."}
