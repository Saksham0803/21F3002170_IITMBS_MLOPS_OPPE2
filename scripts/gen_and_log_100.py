#!/usr/bin/env python3
import os, json, time, random
import numpy as np
import pandas as pd
import requests

# ==== config ====
# Point to your service; use CLUSTER LB IP or local port-forward
API_URL = os.environ.get("API_URL", "http://localhost:8081/predict")
INPUT_CSV = os.environ.get("INPUT_CSV", "data.csv")  # the training data you have
OUT_DIR = "data/generated"
LOG_DIR = "logs"
N = int(os.environ.get("N_SAMPLES", "100"))

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ==== infer feature columns from your dataset ====
df = pd.read_csv(INPUT_CSV)

# Map/rename if your dataset’s columns differ. These match the API schema in app/schemas.py
# If your CSV already has these exact names, this is a no-op. Otherwise, map here.
COLUMN_MAP = {
    # "dataset_col" : "api_field"
    # e.g., "age": "age"
}
if COLUMN_MAP:
    df = df.rename(columns=COLUMN_MAP)

# Identify target column if present
target_candidates = [c for c in df.columns if c.lower() in ("target","label","y")]
target_col = target_candidates[0] if target_candidates else None

# Feature order MUST match app/main.py
feature_cols = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach",
                "exang","oldpeak","slope","ca","thal"]

missing = [c for c in feature_cols if c not in df.columns]
if missing:
    raise ValueError(f"Your data.csv is missing required columns: {missing}")

# ==== sampler for realistic rows (numeric ~ clipped normal; categorical ~ from value counts) ====
def sample_numeric(series: pd.Series) -> float:
    s = series.dropna().astype(float)
    lo, hi = np.percentile(s, [1, 99])
    mu, sd = float(s.mean()), float(s.std() or 1.0)
    x = float(np.clip(np.random.normal(mu, sd), lo, hi))
    # keep ints as ints (for fields like sex, cp, fbs, etc.)
    return int(round(x)) if pd.api.types.is_integer_dtype(series) else x

def sample_categorical(series: pd.Series):
    s = series.dropna()
    vals = s.value_counts(normalize=True)
    return np.random.choice(vals.index, p=vals.values)

def sample_row() -> dict:
    row = {}
    for c in feature_cols:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            row[c] = sample_numeric(s)
        else:
            row[c] = sample_categorical(s)
    # Ensure cast to correct types expected by API (all numeric)
    # (If your dataset has strings for thal, ca, etc., coerce here)
    for c in feature_cols:
        row[c] = float(row[c])
        if c in ("sex","cp","fbs","restecg","exang","slope","ca","thal"):
            row[c] = int(round(row[c]))
    return row

# ==== generate N samples ====
samples = [sample_row() for _ in range(N)]
X = pd.DataFrame(samples, columns=feature_cols)
X.to_csv(f"{OUT_DIR}/test_{N}.csv", index=False)

# ==== call API per-sample and log ====
jsonl_path = f"{LOG_DIR}/predictions_{N}.jsonl"
joined_csv = f"{LOG_DIR}/predictions_with_outputs_{N}.csv"
out_rows = []

session = requests.Session()
for i, r in X.iterrows():
    payload = r.to_dict()
    t0 = time.time()
    resp = session.post(API_URL, json=payload, timeout=5)
    latency = time.time() - t0
    resp.raise_for_status()
    js = resp.json()
    log = {
        "ts": time.time(),
        "index": int(i),
        "latency_s": latency,
        "request": payload,
        "response": js
    }
    out_rows.append({**payload, **js, "latency_s": latency})
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(log) + "\n")

pd.DataFrame(out_rows).to_csv(joined_csv, index=False)
print("[ok] wrote:")
print(f"  - {OUT_DIR}/test_{N}.csv")
print(f"  - {jsonl_path}")
print(f"  - {joined_csv}")
