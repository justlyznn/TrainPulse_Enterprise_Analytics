import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Preprocessing, Training, and Evaluation - TrainPulse
Notebook ini difokuskan pada persiapan data, training beberapa model machine learning, dan evaluasi untuk memprediksi kelulusan training (status_lulus)."""

code_1 = """import sqlite3
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# Load data
base_dir = os.path.dirname(os.path.abspath(''))
db_path = os.path.join(base_dir, 'data', 'trainpulse.db')

conn = sqlite3.connect(db_path)

query = '''
SELECT 
    tp.durasi_hari,
    a.pretest_score, a.status_lulus,
    (SELECT COUNT(*) FROM attendances att WHERE att.session_id = a.session_id AND att.participant_id = a.participant_id AND att.status_hadir = 1) * 1.0 / tp.durasi_hari AS attendance_rate
FROM assessments a
JOIN training_sessions ts ON a.session_id = ts.id
JOIN training_programs tp ON ts.program_id = tp.id
'''

df = pd.read_sql_query(query, conn)
conn.close()

df.head()"""

text_2 = """## Preprocessing & Data Splitting
Memisahkan fitur dan target, serta melakukan train-test split dengan stratifikasi karena kemungkinan kelas target tidak seimbang."""

code_2 = """X = df[['attendance_rate', 'pretest_score', 'durasi_hari']]
y = df['status_lulus'].astype(int)

# Stratified split agar proporsi lulus/tidak lulus seimbang di train dan test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)
print("Class distribution in Train:\\n", y_train.value_counts(normalize=True))"""

text_3 = """## Model Training: Logistic Regression vs Random Forest
Kita akan menggunakan Pipeline untuk memastikan scaling (StandardScaler) diterapkan dengan benar tanpa data leakage."""

code_3 = """# Pipeline 1: Logistic Regression
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('lr', LogisticRegression(random_state=42, class_weight='balanced'))
])

# Pipeline 2: Random Forest
rf_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier(random_state=42, n_estimators=100, class_weight='balanced'))
])

lr_pipeline.fit(X_train, y_train)
rf_pipeline.fit(X_train, y_train)

print("Model Training Complete.")"""

text_4 = """## Evaluation
Membandingkan kinerja kedua model menggunakan Confusion Matrix, Classification Report, dan ROC-AUC."""

code_4 = """def evaluate_model(model, name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    print(f"--- Evaluation for {name} ---")
    print("Classification Report:\\n", classification_report(y_test, y_pred))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}\\n")
    
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix: {name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

evaluate_model(lr_pipeline, "Logistic Regression")
evaluate_model(rf_pipeline, "Random Forest")"""

text_5 = """**Insight Evaluasi:**
- Random Forest biasanya sedikit lebih unggul dalam menangani interaksi antar fitur yang kompleks.
- Logistic Regression memberikan hasil yang mudah diinterpretasikan.
- Kita akan menyimpan Random Forest sebagai model final (atau yang memiliki skor ROC-AUC / F1 tertinggi)."""

text_6 = """## Exporting Final Model
Menyimpan model terbaik beserta preprocessing step-nya ke file `.pkl` menggunakan `joblib`."""

code_6 = """artifacts_dir = os.path.join(base_dir, 'ml', 'artifacts')
os.makedirs(artifacts_dir, exist_ok=True)
model_path = os.path.join(artifacts_dir, 'model.pkl')

# Misalkan kita memilih RandomForest
joblib.dump(rf_pipeline, model_path)
print(f"Final model saved to {model_path}")"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_markdown_cell(text_6),
    nbf.v4.new_code_cell(code_6)
]

with open('notebooks/02_preprocessing_training_eval.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook 02_preprocessing_training_eval.ipynb created.")
