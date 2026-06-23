# TrainPulse Enterprise Analytics

An End-to-End Corporate Learning & Development (L&D) Analytics Platform powered by Machine Learning, FastAPI, and Streamlit. This project serves as a comprehensive portfolio piece demonstrating Fullstack Data Science capabilities.

## 🚀 Key Features (Portfolio Highlights)

1. **Explainable AI (XAI) & Predictive Analytics**
   - Implements a Random Forest Classifier to predict candidate training completion.
   - Extracts and visualizes `feature_importances_` to explain *why* a candidate is predicted to pass or fail, providing actionable business insights.
2. **Bulk Prediction via FastAPI (Batch Processing)**
   - REST API built with FastAPI that includes a `POST /predict/bulk` endpoint.
   - Handles `multipart/form-data` CSV uploads, processes hundreds of candidates instantly, and returns scored data.
3. **Advanced SQL Analytics**
   - Features an Instructor Performance Leaderboard generated using complex SQLite queries (`JOIN`, `GROUP BY`, `HAVING`).
4. **Premium Streamlit Dashboard**
   - Multi-page navigation (Executive Summary, Deep Dive Analytics, AI Predictor Hub).
   - Interactive visualizations utilizing Plotly and Custom CSS (Dark Theme, Glassmorphism).

## 🛠️ Tech Stack

- **Machine Learning**: `scikit-learn`, `pandas`
- **Backend API**: `FastAPI`, `Uvicorn`, `Pydantic`
- **Database**: `SQLite` (with `SQLAlchemy` ORM)
- **Frontend / Dashboard**: `Streamlit`, `Plotly`

## 📂 Project Structure

```text
TrainPulse/
├── api/                   # FastAPI backend implementation (Routers, Models, Schemas)
├── core/                  # Core Business Logic (ML Inference Singleton, SQLite Queries)
├── data/                  # SQLite database storage
├── ml/                    # Data Generation scripts & Saved Models (.pkl)
├── notebooks/             # Jupyter Notebooks for EDA and Model Training
├── streamlit_app/         # Frontend Streamlit Dashboard
├── tests/                 # Pytest suite for unit testing
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## ⚙️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/justlyznn/TrainPulse_Enterprise_Analytics.git
   cd TrainPulse_Enterprise_Analytics
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Run the FastAPI Backend:**
   ```bash
   uvicorn api.main:app --reload
   # The API will be available at http://127.0.0.1:8000
   # Swagger UI available at http://127.0.0.1:8000/docs
   ```

4. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run streamlit_app/app.py
   # The Dashboard will be available at http://localhost:8501
   ```

## 🌐 Deploying to Streamlit Community Cloud

When deploying this project to Streamlit Community Cloud:
1. Select the GitHub repository.
2. Set the Main file path to: `streamlit_app/app.py`
3. Click Deploy!

---
*Created as a comprehensive demonstration of End-to-End Data Science and Software Engineering.*
