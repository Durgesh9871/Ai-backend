from fastapi import FastAPI
    
from app.api.health import router as health_router
from app.api.v1.events import router as events_router

app = FastAPI(
    title="AI SeatFlow Ticket System",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(events_router)