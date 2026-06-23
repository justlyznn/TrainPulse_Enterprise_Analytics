import os
import joblib
import pandas as pd

class MLInference:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLInference, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'ml', 'artifacts', 'model.pkl')
        try:
            self._model = joblib.load(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            self._model = None

    def predict_completion(self, attendance_rate: float, pretest_score: float, durasi_hari: int):
        if not self._model:
            raise ValueError("Model is not loaded.")
        
        # Buat DataFrame sesuai dengan input yang digunakan saat training
        input_data = pd.DataFrame([{
            'attendance_rate': attendance_rate,
            'pretest_score': pretest_score,
            'durasi_hari': durasi_hari
        }])

        prob = self._model.predict_proba(input_data)[0][1]
        label = self._model.predict(input_data)[0]
        
        # Extract Feature Importances (XAI)
        rf_model = self._model.named_steps.get('rf')
        feature_importances = {}
        if rf_model is not None:
            importances = rf_model.feature_importances_
            feature_importances = {
                'Attendance Rate': float(importances[0]),
                'Pretest Score': float(importances[1]),
                'Durasi Hari': float(importances[2])
            }
        
        return {
            'probability': float(prob),
            'status_lulus': bool(label),
            'feature_importances': feature_importances
        }

# Inisialisasi instance singleton
inference_service = MLInference()

def predict(attendance_rate: float, pretest_score: float, durasi_hari: int):
    return inference_service.predict_completion(attendance_rate, pretest_score, durasi_hari)
