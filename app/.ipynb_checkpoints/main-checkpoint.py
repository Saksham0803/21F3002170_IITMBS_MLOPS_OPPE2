import os
import time
import joblib
import numpy as np
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest
from app.schemas import HeartRequest, HeartResponse

MODEL_PATH = os.getenv("MODEL_PATH", "models/heart.joblib")

app = FastAPI(title="Heart Disease API")

# metrics
PRED_COUNT = Counter("predictions_total", "Total predictions served")
PRED_LAT   = Histogram("prediction_latency_seconds", "Latency of /predict")

# model
model = None

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(MODEL_PATH)

@app.get("/healthz")
def health():
    # quick check: model loaded
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()

@app.post("/predict", response_model=HeartResponse)
def predict(req: HeartRequest):
    start = time.time()
    # keep feature order EXACTLY as in training
    X = np.array([[req.age, req.sex, req.cp, req.trestbps, req.chol, req.fbs,
                   req.restecg, req.thalach, req.exang, req.oldpeak, req.slope,
                   req.ca, req.thal]], dtype=float)
    proba = float(model.predict_proba(X)[0, 1])
    pred = int(proba >= 0.5)
    PRED_COUNT.inc()
    PRED_LAT.observe(time.time() - start)
    return HeartResponse(prediction=pred, probability=proba)
