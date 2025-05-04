from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.TicketResponse])
def list_user_tickets(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    tickets = db.query(models.Ticket).filter(models.Ticket.user_id == current_user.id).all()
    return [
        schemas.TicketResponse(
            **ticket.__dict__,
            event_title=ticket.event.title,
            event_date=ticket.event.date
        ) for ticket in tickets
    ]

@router.get("/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(
    ticket_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.id == ticket_id,
        models.Ticket.user_id == current_user.id
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return schemas.TicketResponse(
        **ticket.__dict__,
        event_title=ticket.event.title,
        event_date=ticket.event.date
    )

@router.post("/{ticket_id}/validate", response_model=schemas.TicketResponse)
def validate_ticket(
    ticket_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    if ticket.status != "active":
        raise HTTPException(status_code=400, detail="Ticket is not active")
    
    ticket.status = "used"
    db.commit()
    db.refresh(ticket)
    
    return schemas.TicketResponse(
        **ticket.__dict__,
        event_title=ticket.event.title,
        event_date=ticket.event.date
    ) 