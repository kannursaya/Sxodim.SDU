from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.ClubResponse])
def list_clubs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    clubs = db.query(models.Club).offset(skip).limit(limit).all()
    return [
        schemas.ClubResponse(
            **club.__dict__,
            member_count=len(club.members)
        ) for club in clubs
    ]

@router.post("/", response_model=schemas.ClubResponse)
def create_club(
    club: schemas.ClubCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_club = models.Club(**club.dict())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    
    # Add creator as admin
    membership = models.ClubMembership(
        user_id=current_user.id,
        club_id=db_club.id,
        role="admin"
    )
    db.add(membership)
    db.commit()
    
    return schemas.ClubResponse(
        **db_club.__dict__,
        member_count=1
    )

@router.get("/{club_id}", response_model=schemas.ClubResponse)
def get_club(
    club_id: int,
    db: Session = Depends(get_db)
):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    return schemas.ClubResponse(
        **club.__dict__,
        member_count=len(club.members)
    )

@router.post("/{club_id}/join", response_model=schemas.ClubMembershipResponse)
def join_club(
    club_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    club = db.query(models.Club).filter(models.Club.id == club_id).first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    
    existing_membership = db.query(models.ClubMembership).filter(
        models.ClubMembership.user_id == current_user.id,
        models.ClubMembership.club_id == club_id
    ).first()
    
    if existing_membership:
        raise HTTPException(status_code=400, detail="Already a member of this club")
    
    membership = models.ClubMembership(
        user_id=current_user.id,
        club_id=club_id,
        role="member"
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    
    return schemas.ClubMembershipResponse(
        **membership.__dict__,
        club_name=club.name
    ) 