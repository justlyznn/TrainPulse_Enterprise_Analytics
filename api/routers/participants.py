from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/participants",
    tags=["participants"]
)

@router.get("/", response_model=List[schemas.Participant])
def read_participants(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    participants = db.query(models.Participant).offset(skip).limit(limit).all()
    return participants

@router.post("/", response_model=schemas.Participant)
def create_participant(participant: schemas.ParticipantCreate, db: Session = Depends(database.get_db)):
    db_participant = models.Participant(**participant.model_dump())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

@router.get("/{participant_id}", response_model=schemas.Participant)
def read_participant(participant_id: int, db: Session = Depends(database.get_db)):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant
