from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.EventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return [
        schemas.EventResponse(
            **event.__dict__,
            tickets_sold=len(event.tickets)
        ) for event in events
    ]

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return schemas.EventResponse(
        **db_event.__dict__,
        tickets_sold=0
    )

@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return schemas.EventResponse(
        **event.__dict__,
        tickets_sold=len(event.tickets)
    )

@router.post("/{event_id}/tickets", response_model=schemas.TicketResponse)
def purchase_ticket(
    event_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if len(event.tickets) >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is full")
    
    ticket = models.Ticket(
        user_id=current_user.id,
        event_id=event_id,
        status="active"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    
    return schemas.TicketResponse(
        **ticket.__dict__,
        event_title=event.title,
        event_date=event.date
    ) 