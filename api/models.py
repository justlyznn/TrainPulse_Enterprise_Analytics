from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from .database import Base

class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String, index=True)
    departemen = Column(String, index=True)
    tanggal_join = Column(Date)

class TrainingProgram(Base):
    __tablename__ = 'training_programs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama_program = Column(String, index=True)
    kategori = Column(String, index=True)
    durasi_hari = Column(Integer)

class TrainingSession(Base):
    __tablename__ = 'training_sessions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey('training_programs.id'))
    batch = Column(Integer)
    tanggal_mulai = Column(Date)
    instruktur = Column(String)

class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('training_sessions.id'))
    participant_id = Column(Integer, ForeignKey('participants.id'))
    tanggal = Column(Date)
    status_hadir = Column(Boolean)

class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('training_sessions.id'))
    participant_id = Column(Integer, ForeignKey('participants.id'))
    pretest_score = Column(Float)
    posttest_score = Column(Float)
    status_lulus = Column(Boolean)
