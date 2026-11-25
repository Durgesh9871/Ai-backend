from fastapi import APIRouter, Request, Depends, status, HTTPException, Response
from app.schema.events import EventCreate, EventResponse, EventUpdate
from uuid import uuid4,UUID
# from logging import getLogger
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1/events", tags=["events"])

event_store: dict[UUID, EventResponse] = {}

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate) -> EventResponse:

    event = EventResponse(
        id=uuid4(),
        **payload.model_dump()
    )

    event_store[event.id] = event
    logger.info(f"Event created: {event}" , extra={"event_store": event_store})
    
    return event

        
    
@router.get("", response_model=list[EventResponse])
async def get_events() -> list[EventResponse]:
    return list(event_store.values())



@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: UUID) -> EventResponse:
    if not event_id in event_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event_store[event_id]



@router.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: UUID , payload: EventCreate) -> EventResponse:
    if not event_id in event_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    updated_event = EventResponse(
        id=event_id,
        **payload.model_dump()
    )

    event_store[event_id] = updated_event
    
    return updated_event
    

@router.patch("/{event_id}" , response_model=EventResponse)
def update_event_partial(event_id: UUID , payload: EventUpdate) -> EventResponse:
    
    current_event = event_store.get(event_id)

    if not current_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    update_data = payload.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    updated_event = current_event.model_copy(update=update_data)
    event_store[event_id] = updated_event
    
    return updated_event
    
    
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: UUID) -> Response:
    if not event_id in event_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    del event_store[event_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)