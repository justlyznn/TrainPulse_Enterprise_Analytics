from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

@router.get("/", response_model=List[schemas.TrainingSession])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    sessions = db.query(models.TrainingSession).offset(skip).limit(limit).all()
    return sessions

@router.post("/", response_model=schemas.TrainingSession)
def create_session(session: schemas.TrainingSessionCreate, db: Session = Depends(database.get_db)):
    db_session = models.TrainingSession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/{session_id}", response_model=schemas.TrainingSession)
def read_session(session_id: int, db: Session = Depends(database.get_db)):
    session = db.query(models.TrainingSession).filter(models.TrainingSession.id == session_id).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
