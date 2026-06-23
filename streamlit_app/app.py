import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import io

# Menambahkan parent directory ke PYTHONPATH agar bisa mengimport 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import queries, ml_inference

st.set_page_config(page_title="TrainPulse Hub", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS untuk Premium Look (Glassmorphism & Typography) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(to bottom right, #0F172A, #1E293B);
        color: #F8FAFC;
    }
    
    /* Custom Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Metric Cards Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: rgba(56, 189, 248, 0.5);
    }

    .stButton>button {
        background: linear-gradient(90deg, #38BDF8 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
    }
    
    h1, h2, h3 {
        color: #F8FAFC !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.markdown("## **TrainPulse**")
st.sidebar.markdown("Corporate L&D Analytics Engine")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigasi",
    ("Executive Summary", "Deep Dive Analytics", "AI Predictor Hub")
)

st.sidebar.divider()
st.sidebar.caption("© 2026 TrainPulse Inc.")

# --- PAGE 1: Executive Summary ---
if menu == "Executive Summary":
    st.markdown('<p class="main-header">Executive Summary</p>', unsafe_allow_html=True)
    st.markdown("Overview metrik utama dan aktivitas pelatihan terbaru.")
    st.write("")
    
    kpis = queries.get_overall_kpis()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Attendance Rate", f"{kpis['attendance_rate']*100:.1f}%", "↑ 2% vs Last Quarter")
    with col2:
        st.metric("Avg Completion Rate", f"{kpis['completion_rate']*100:.1f}%", "↑ 5% vs Last Quarter")
    with col3:
        st.metric("Active Programs", "5", "Stable")
        
    st.write("---")
    
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Tren Kehadiran Harian")
        trend_data = queries.get_attendance_trend()
        if trend_data:
            df_trend = pd.DataFrame(trend_data)
            df_trend['tanggal'] = pd.to_datetime(df_trend['tanggal'])
            
            # Smoothing data: Agregasi rata-rata per bulan agar tidak terlalu "berantakan" (jagged)
            df_trend_monthly = df_trend.set_index('tanggal').resample('ME').mean().reset_index()
            
            fig_trend = px.area(df_trend_monthly, x='tanggal', y='daily_attendance_rate', 
                                color_discrete_sequence=['#38BDF8'],
                                template='plotly_dark',
                                markers=True,
                                labels={'tanggal': 'Bulan', 'daily_attendance_rate': 'Rata-rata Kehadiran'})
            
            # Membuat garis lebih smooth
            fig_trend.update_traces(line_shape='spline')
            
            fig_trend.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                    margin=dict(l=0, r=0, t=30, b=0))
            fig_trend.update_yaxes(range=[0, 1])
            st.plotly_chart(fig_trend, use_container_width=True)
            
    with col_chart2:
        st.subheader("Status Kelulusan")
        dist_data = queries.get_pass_fail_distribution()
        if dist_data:
            df_dist = pd.DataFrame(dist_data)
            fig_donut = px.pie(df_dist, values='count', names='status', hole=0.7,
                               color='status', color_discrete_map={'Lulus':'#34D399', 'Tidak Lulus':'#F87171'},
                               template='plotly_dark')
            fig_donut.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)

    st.subheader("Aktivitas Sesi Terakhir")
    recent_data = queries.get_recent_assessments(limit=10)
    if recent_data:
        df_recent = pd.DataFrame(recent_data)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)

# --- PAGE 2: Deep Dive Analytics ---
elif menu == "Deep Dive Analytics":
    st.markdown('<p class="main-header">Deep Dive Analytics</p>', unsafe_allow_html=True)
    st.markdown("Analisis komparatif berdasarkan departemen, kategori program, dan performa instruktur.")
    st.write("---")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.subheader("Completion Rate by Kategori")
        cat_data = queries.get_completion_by_category()
        if cat_data:
            df_cat = pd.DataFrame(cat_data)
            df_cat = df_cat.sort_values(by='completion_rate', ascending=True)
            fig_cat = px.bar(df_cat, x='completion_rate', y='kategori', orientation='h',
                             color='completion_rate', color_continuous_scale='Blues',
                             template='plotly_dark')
            fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_cat, use_container_width=True)
            
    with col_d2:
        st.subheader("Attendance Rate by Departemen")
        dept_data = queries.get_attendance_by_department()
        if dept_data:
            df_dept = pd.DataFrame(dept_data)
            fig_dept = px.bar(df_dept, x='departemen', y='attendance_rate',
                              color='attendance_rate', color_continuous_scale='Teal',
                              template='plotly_dark')
            fig_dept.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_dept, use_container_width=True)
            
    st.write("---")
    st.subheader("Instructor Performance Leaderboard")
    inst_data = queries.get_instructor_leaderboard()
    if inst_data:
        df_inst = pd.DataFrame(inst_data)
        # Format percentages and scores
        df_inst['Completion_Rate'] = (df_inst['Completion_Rate'] * 100).map('{:.1f}%'.format)
        df_inst['Avg_Posttest'] = df_inst['Avg_Posttest'].map('{:.1f}'.format)
        st.dataframe(df_inst, use_container_width=True, hide_index=True)

# --- PAGE 3: AI Predictor Hub ---
elif menu == "AI Predictor Hub":
    st.markdown('<p class="main-header">AI Predictor Hub</p>', unsafe_allow_html=True)
    st.markdown("Gunakan model Machine Learning (Random Forest) untuk memprediksi kelulusan kandidat.")
    st.write("---")
    
    tab1, tab2 = st.tabs(["Single Prediction & XAI", "Bulk Prediction (CSV Upload)"])
    
    with tab1:
        col_form, col_result = st.columns([1, 1])
        
        with col_form:
            st.markdown("### Input Parameter")
            attendance_rate = st.slider("Attendance Rate", min_value=0.0, max_value=1.0, value=0.85, step=0.05,
                                        help="Persentase kehadiran karyawan pada sesi training (0.0 - 1.0)")
            pretest_score = st.number_input("Pretest Score", min_value=0.0, max_value=100.0, value=65.0,
                                            help="Nilai pretest sebelum training dimulai")
            durasi_hari = st.number_input("Durasi Hari Program", min_value=1, max_value=30, value=5,
                                          help="Total durasi training dalam hitungan hari")
            
            predict_btn = st.button("Generate Prediction")

        with col_result:
            st.markdown("### Hasil Prediksi")
            if predict_btn:
                with st.spinner("Analyzing parameters..."):
                    try:
                        result = ml_inference.predict(
                            attendance_rate=attendance_rate,
                            pretest_score=pretest_score,
                            durasi_hari=durasi_hari
                        )
                        
                        prob = result['probability'] * 100
                        
                        if result['status_lulus']:
                            st.success("**KANDIDAT KEMUNGKINAN BESAR LULUS**")
                            st.progress(result['probability'])
                            st.markdown(f"<h1 style='text-align: center; color: #34D399;'>{prob:.1f}%</h1>", unsafe_allow_html=True)
                        else:
                            st.error("**KANDIDAT BERISIKO TIDAK LULUS**")
                            st.progress(result['probability'])
                            st.markdown(f"<h1 style='text-align: center; color: #F87171;'>{prob:.1f}%</h1>", unsafe_allow_html=True)
                            
                        # Explainable AI (XAI) Chart
                        importances = result.get('feature_importances', {})
                        if importances:
                            st.markdown("#### Faktor Penentu Prediksi (Feature Importances)")
                            df_imp = pd.DataFrame(list(importances.items()), columns=['Fitur', 'Kepentingan'])
                            df_imp = df_imp.sort_values(by='Kepentingan', ascending=True)
                            fig_imp = px.bar(df_imp, x='Kepentingan', y='Fitur', orientation='h',
                                             template='plotly_dark', color_discrete_sequence=['#818CF8'])
                            fig_imp.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0),
                                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                            st.plotly_chart(fig_imp, use_container_width=True)
                            
                    except Exception as e:
                        st.error(f"Error dalam memprediksi: {e}")
            else:
                st.info("Silakan sesuaikan parameter di sebelah kiri dan klik tombol prediksi.")
                
    with tab2:
        st.markdown("### Bulk Prediction (Scoring Batch Kandidat)")
        st.markdown("Upload file CSV berisi kolom: `attendance_rate`, `pretest_score`, `durasi_hari`")
        
        use_dummy = st.button("Gunakan Data Dummy (Testing)")
        uploaded_file = st.file_uploader("Atau pilih file CSV dari komputer Anda", type=["csv"])
        
        df_upload = None
        
        if use_dummy:
            try:
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                dummy_path = os.path.join(base_dir, 'sample_batch.csv')
                df_upload = pd.read_csv(dummy_path)
                st.info("Menggunakan data dummy 'sample_batch.csv'")
            except Exception as e:
                st.error(f"Gagal memuat data dummy: {e}")
        elif uploaded_file is not None:
            try:
                df_upload = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Gagal membaca file CSV: {e}")
                
        if df_upload is not None:
            required_cols = {'attendance_rate', 'pretest_score', 'durasi_hari'}
            
            if not required_cols.issubset(df_upload.columns):
                st.error(f"Format data tidak valid! Harus mengandung kolom: {required_cols}")
            else:
                st.success("Data berhasil dibaca. Prediksi Selesai!")
                
                results = []
                for idx, row in df_upload.iterrows():
                    res = ml_inference.predict(
                        attendance_rate=row['attendance_rate'],
                        pretest_score=row['pretest_score'],
                        durasi_hari=row['durasi_hari']
                    )
                    label = "Lulus" if res['status_lulus'] else "Tidak Lulus"
                    
                    row_dict = row.to_dict()
                    row_dict['Probability (%)'] = round(res['probability'] * 100, 2)
                    row_dict['Prediction'] = label
                    results.append(row_dict)
                    
                df_results = pd.DataFrame(results)
                
                st.write("---")
                col_chart, col_table = st.columns([1, 2])
                
                with col_chart:
                    st.markdown("#### Proporsi Prediksi Kelulusan")
                    fig_pie = px.pie(df_results, names='Prediction', hole=0.6, 
                                     color='Prediction', color_discrete_map={'Lulus':'#34D399', 'Tidak Lulus':'#F87171'},
                                     template='plotly_dark')
                    fig_pie.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=True)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col_table:
                    st.markdown("#### Detail Hasil Prediksi")
                    st.dataframe(df_results, use_container_width=True)
                
                # Sediakan opsi download
                csv = df_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Hasil Prediksi CSV",
                    data=csv,
                    file_name='bulk_predictions_result.csv',
                    mime='text/csv',
                )
