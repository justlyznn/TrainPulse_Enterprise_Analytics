import sqlite3
import pandas as pd
import os

def get_db_connection():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'trainpulse.db')
    return sqlite3.connect(db_path)

def get_overall_kpis():
    conn = get_db_connection()
    # Completion Rate
    query_completion = "SELECT AVG(status_lulus) as completion_rate FROM assessments"
    df_completion = pd.read_sql_query(query_completion, conn)
    
    # Attendance Rate
    query_attendance = '''
    SELECT AVG(status_hadir) as attendance_rate 
    FROM attendances
    '''
    df_attendance = pd.read_sql_query(query_attendance, conn)
    
    conn.close()
    return {
        "completion_rate": float(df_completion['completion_rate'][0] or 0),
        "attendance_rate": float(df_attendance['attendance_rate'][0] or 0)
    }

def get_attendance_trend():
    conn = get_db_connection()
    query = '''
    SELECT tanggal, AVG(status_hadir) as daily_attendance_rate
    FROM attendances
    GROUP BY tanggal
    ORDER BY tanggal
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

def get_completion_by_category():
    conn = get_db_connection()
    query = '''
    SELECT tp.kategori, AVG(a.status_lulus) as completion_rate
    FROM assessments a
    JOIN training_sessions ts ON a.session_id = ts.id
    JOIN training_programs tp ON ts.program_id = tp.id
    GROUP BY tp.kategori
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

def get_attendance_by_department():
    conn = get_db_connection()
    query = '''
    SELECT p.departemen, AVG(att.status_hadir) as attendance_rate
    FROM attendances att
    JOIN participants p ON att.participant_id = p.id
    GROUP BY p.departemen
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

def get_recent_assessments(limit=50):
    conn = get_db_connection()
    query = f'''
    SELECT p.nama as "Nama Peserta", p.departemen as "Departemen", 
           tp.nama_program as "Program", ts.batch as "Batch", 
           a.pretest_score as "Pretest", a.posttest_score as "Posttest", 
           CASE WHEN a.status_lulus = 1 THEN 'Lulus' ELSE 'Tidak Lulus' END as "Status"
    FROM assessments a
    JOIN participants p ON a.participant_id = p.id
    JOIN training_sessions ts ON a.session_id = ts.id
    JOIN training_programs tp ON ts.program_id = tp.id
    ORDER BY a.id DESC
    LIMIT {limit}
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

def get_pass_fail_distribution():
    conn = get_db_connection()
    query = '''
    SELECT 
        CASE WHEN status_lulus = 1 THEN 'Lulus' ELSE 'Tidak Lulus' END as status,
        COUNT(*) as count
    FROM assessments
    GROUP BY status_lulus
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')

def get_instructor_leaderboard():
    conn = get_db_connection()
    query = '''
    SELECT 
        ts.instruktur as Instructor,
        COUNT(DISTINCT ts.id) as Total_Sessions,
        COUNT(a.id) as Total_Participants,
        AVG(a.posttest_score) as Avg_Posttest,
        AVG(a.status_lulus) as Completion_Rate
    FROM training_sessions ts
    JOIN assessments a ON ts.id = a.session_id
    GROUP BY ts.instruktur
    HAVING Total_Participants > 5
    ORDER BY Completion_Rate DESC, Avg_Posttest DESC
    LIMIT 10
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient='records')
