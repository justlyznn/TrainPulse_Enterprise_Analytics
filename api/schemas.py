from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class ParticipantBase(BaseModel):
    nama: str
    departemen: str
    tanggal_join: date

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TrainingProgramBase(BaseModel):
    nama_program: str
    kategori: str
    durasi_hari: int

class TrainingProgramCreate(TrainingProgramBase):
    pass

class TrainingProgram(TrainingProgramBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TrainingSessionBase(BaseModel):
    program_id: int
    batch: int
    tanggal_mulai: date
    instruktur: str

class TrainingSessionCreate(TrainingSessionBase):
    pass

class TrainingSession(TrainingSessionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PredictCompletionRequest(BaseModel):
    attendance_rate: float
    pretest_score: float
    durasi_hari: int

class PredictCompletionResponse(BaseModel):
    probability: float
    status_lulus: bool
    label: str
    feature_importances: dict = None
