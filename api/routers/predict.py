from fastapi import APIRouter, UploadFile, File
import pandas as pd
from typing import List
from io import StringIO
from .. import schemas
from core import ml_inference

router = APIRouter(
    prefix="/predict",
    tags=["predict"]
)

@router.post("/completion", response_model=schemas.PredictCompletionResponse)
def predict_completion(request: schemas.PredictCompletionRequest):
    result = ml_inference.predict(
        attendance_rate=request.attendance_rate,
        pretest_score=request.pretest_score,
        durasi_hari=request.durasi_hari
    )
    
    label = "Lulus" if result['status_lulus'] else "Tidak Lulus"
    
    return schemas.PredictCompletionResponse(
        probability=result['probability'],
        status_lulus=result['status_lulus'],
        label=label,
        feature_importances=result.get('feature_importances', {})
    )

@router.post("/bulk")
async def bulk_predict(file: UploadFile = File(...)):
    contents = await file.read()
    csv_str = contents.decode("utf-8")
    df = pd.read_csv(StringIO(csv_str))
    
    # Validasi kolom minimal
    required_cols = {'attendance_rate', 'pretest_score', 'durasi_hari'}
    if not required_cols.issubset(df.columns):
        return {"error": f"CSV harus memiliki kolom: {required_cols}"}
    
    results = []
    for _, row in df.iterrows():
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
        
    return {"data": results}
