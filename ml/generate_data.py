import os
import random
from datetime import timedelta, date
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from faker import Faker

# Setup Database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, 'trainpulse.db')

engine = create_engine(f'sqlite:///{DB_PATH}')
Base = declarative_base()

# Models
class Participant(Base):
    __tablename__ = 'participants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String)
    departemen = Column(String)
    tanggal_join = Column(Date)

class TrainingProgram(Base):
    __tablename__ = 'training_programs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama_program = Column(String)
    kategori = Column(String)
    durasi_hari = Column(Integer)

class TrainingSession(Base):
    __tablename__ = 'training_sessions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey('training_programs.id'))
    batch = Column(Integer)
    tanggal_mulai = Column(Date)
    instruktur = Column(String)

class Attendance(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('training_sessions.id'))
    participant_id = Column(Integer, ForeignKey('participants.id'))
    tanggal = Column(Date)
    status_hadir = Column(Boolean)

class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('training_sessions.id'))
    participant_id = Column(Integer, ForeignKey('participants.id'))
    pretest_score = Column(Float)
    posttest_score = Column(Float)
    status_lulus = Column(Boolean)

def generate_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    fake = Faker('id_ID')

    print("Generating data...")

    # 1. Generate Participants
    departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations']
    participants = []
    for _ in range(1000):
        p = Participant(
            nama=fake.name(),
            departemen=random.choice(departments),
            tanggal_join=fake.date_between(start_date='-5y', end_date='today')
        )
        session.add(p)
        participants.append(p)
    session.commit()

    # 2. Generate Training Programs
    programs_data = [
        ("Effective Communication", "Soft Skills", 3),
        ("Leadership 101", "Leadership", 5),
        ("Python for Data Science", "Technical", 10),
        ("Workplace Safety", "Compliance", 2),
        ("New Employee Onboarding", "Onboarding", 4)
    ]
    programs = []
    for nama, kat, durasi in programs_data:
        prog = TrainingProgram(nama_program=nama, kategori=kat, durasi_hari=durasi)
        session.add(prog)
        programs.append(prog)
    session.commit()

    # 3. Generate Training Sessions
    sessions = []
    for prog in programs:
        for batch in range(1, 11): # 10 batch per program
            ts = TrainingSession(
                program_id=prog.id,
                batch=batch,
                tanggal_mulai=fake.date_between(start_date='-2y', end_date='today'),
                instruktur=fake.name()
            )
            session.add(ts)
            sessions.append(ts)
    session.commit()

    # 4. Generate Attendances & Assessments
    for ts in sessions:
        prog = session.query(TrainingProgram).get(ts.program_id)
        # Randomly select 20-40 participants for this session
        session_participants = random.sample(participants, random.randint(20, 40))
        
        for p in session_participants:
            # Generate Attendance
            hadir_count = 0
            
            # BIAS: Departemen Operations sibuk, probabilitas hadir lebih rendah
            dept_penalty = 0.2 if p.departemen == 'Operations' else 0.0
            
            # BIAS: Program Compliance (wajib tapi membosankan) punya base drop-off tinggi
            prog_penalty = 0.15 if prog.kategori == 'Compliance' else 0.0
            
            for day in range(prog.durasi_hari):
                tgl = ts.tanggal_mulai + timedelta(days=day)
                
                # Base probability of attending
                base_prob = random.uniform(0.6, 0.95)
                
                # BIAS: Jumat malas (weekday == 4 adalah Jumat)
                day_penalty = 0.2 if tgl.weekday() == 4 else 0.0
                
                # BIAS: Makin lama durasi hari, peserta makin jenuh (drop-off over time)
                fatigue_penalty = (day / prog.durasi_hari) * 0.15
                
                final_prob = base_prob - dept_penalty - prog_penalty - day_penalty - fatigue_penalty
                
                is_hadir = random.random() < final_prob
                if is_hadir: hadir_count += 1
                
                att = Attendance(
                    session_id=ts.id,
                    participant_id=p.id,
                    tanggal=tgl,
                    status_hadir=is_hadir
                )
                session.add(att)
            
            # Generate Assessment
            attendance_rate = hadir_count / prog.durasi_hari
            
            # BIAS: Peserta Technical biasanya pretest lebih rendah krn materi sulit
            if prog.kategori == 'Technical':
                pretest = random.uniform(20, 60)
            else:
                pretest = random.uniform(40, 80)
            
            # Posttest depends highly on attendance + randomness
            # Jika attendance < 50%, ilmu tidak terserap
            if attendance_rate < 0.5:
                improvement_factor = random.uniform(-5, 10) # Bisa malah turun/lupa
            else:
                improvement_factor = random.uniform(10, 40)
                
            posttest = pretest + (attendance_rate * improvement_factor) + random.uniform(-10, 10)
            posttest = min(max(posttest, 0), 100) # Clamp between 0 and 100
            
            status_lulus = posttest >= 70.0
            
            assmnt = Assessment(
                session_id=ts.id,
                participant_id=p.id,
                pretest_score=round(pretest, 2),
                posttest_score=round(posttest, 2),
                status_lulus=status_lulus
            )
            session.add(assmnt)
            
    session.commit()
    print(f"Data generation complete. Database saved to: {DB_PATH}")

if __name__ == "__main__":
    generate_data()
