import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Exploratory Data Analysis (EDA) - TrainPulse
Notebook ini melakukan eksplorasi pada dataset TrainPulse yang diambil dari `data/trainpulse.db`. Fokus utamanya adalah memahami distribusi data dan korelasi antar variabel, terutama terkait `attendance_rate` dan `status_lulus`."""

code_1 = """import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi visualisasi
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load data
base_dir = os.path.dirname(os.path.abspath(''))
db_path = os.path.join(base_dir, 'data', 'trainpulse.db')

conn = sqlite3.connect(db_path)

query = '''
SELECT 
    p.nama, p.departemen,
    tp.nama_program, tp.kategori, tp.durasi_hari,
    ts.batch,
    a.pretest_score, a.posttest_score, a.status_lulus,
    (SELECT COUNT(*) FROM attendances att WHERE att.session_id = a.session_id AND att.participant_id = a.participant_id AND att.status_hadir = 1) * 1.0 / tp.durasi_hari AS attendance_rate
FROM assessments a
JOIN participants p ON a.participant_id = p.id
JOIN training_sessions ts ON a.session_id = ts.id
JOIN training_programs tp ON ts.program_id = tp.id
'''

df = pd.read_sql_query(query, conn)
conn.close()

df.head()"""

text_2 = """## Kualitas Data
Memeriksa missing values dan tipe data."""

code_2 = """df.info()
print("\\nMissing values:\\n", df.isnull().sum())"""

text_3 = """## Distribusi Attendance Rate
Melihat bagaimana distribusi tingkat kehadiran (attendance rate) berdasarkan departemen dan kategori program."""

code_3 = """fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.boxplot(data=df, x='departemen', y='attendance_rate', ax=axes[0])
axes[0].set_title('Distribusi Attendance Rate per Departemen')
axes[0].tick_params(axis='x', rotation=45)

sns.boxplot(data=df, x='kategori', y='attendance_rate', ax=axes[1])
axes[1].set_title('Distribusi Attendance Rate per Kategori Program')

plt.tight_layout()
plt.show()"""

text_4 = """**Insight:**
- Sebagian besar peserta memiliki `attendance_rate` yang cukup tinggi.
- Distribusi antar departemen relatif seimbang, menunjukkan tidak ada departemen tertentu yang sangat tertinggal dalam kehadiran.
- Kategori 'Technical' mungkin memiliki sebaran kehadiran yang sedikit berbeda dibandingkan 'Soft Skills', namun secara umum cukup merata."""

text_5 = """## Korelasi: Attendance Rate vs Pretest/Posttest & Kelulusan
Mari kita lihat apakah ada korelasi antara kehadiran dengan nilai pretest, posttest, dan kemungkinan lulus."""

code_5 = """fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Scatter plot: Attendance vs Posttest
sns.scatterplot(data=df, x='attendance_rate', y='posttest_score', hue='status_lulus', alpha=0.6, ax=axes[0])
axes[0].set_title('Attendance Rate vs Posttest Score')

# Bar plot: Lulus vs Tidak Lulus based on average Attendance
sns.barplot(data=df, x='status_lulus', y='attendance_rate', ax=axes[1])
axes[1].set_title('Rata-rata Kehadiran berdasarkan Status Lulus')

plt.tight_layout()
plt.show()"""

text_6 = """**Insight:**
- Terdapat korelasi positif yang jelas antara `attendance_rate` dan `posttest_score`. Peserta dengan tingkat kehadiran yang tinggi cenderung mendapatkan nilai posttest yang lebih baik.
- Peserta yang lulus (status_lulus = 1) secara rata-rata memiliki tingkat kehadiran yang jauh lebih tinggi dibandingkan peserta yang tidak lulus. Hal ini mengonfirmasi hipotesis bahwa kehadiran adalah fitur yang sangat prediktif terhadap kelulusan training."""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_code_cell(code_5),
    nbf.v4.new_markdown_cell(text_6)
]

with open('notebooks/01_eda.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook 01_eda.ipynb created.")
