# 21F3002170_IITMBS_MLOPS_OPPE2

Submission for **OPPE2 (MLOps)** – IITM BS Program.  
This project demonstrates an **end-to-end production-ready deployment** for a **Heart Disease Prediction** system with explainability, fairness, observability, scalability, performance monitoring, drift detection, and robustness testing.

---

## 📁 Repository Structure

- `HeartDiseaseTrainingAndPrediction.ipynb` – Extended training notebook with all tasks  
- `data.csv` – Provided training dataset  
- `data/generated/` – Synthetic datasets for testing and monitoring  
- `models/` – Trained models, SHAP outputs, drift reports  
- `app/` – FastAPI application code (API server)  
- `k8s/` – Kubernetes manifests (Deployment, Service, HPA)  
- `perf/` – Load-testing scripts (`post.lua`) and wrk results  
- `logs/` – Logs of predictions, monitoring, drift, poisoning experiments  
- `Dockerfile`, `requirements.txt` – Containerization setup  
- `README.md` – This file  

---

## 1️⃣ GitHub Setup

- Created a private repo: **21F3002170_IITMBS_MLOPS_OPPE2**  
- Added IITMBSMLOps as collaborator  
- Configured SSH authentication from GCP VM  
- Structured commits after each integration stage with meaningful messages  

---

## 2️⃣ Explainability (10 marks)

We used **SHAP** to interpret the Logistic Regression model.

- **Global importance**: `oldpeak`, `thalach`, `trestbps`, `chol`, and `age` strongly influence predictions.  
- **Local explanations**: For positive predictions, SHAP identified top 5 contributing features per patient.  

✅ Outputs:  
- `models/shap_summary.png` – beeswarm summary  
- `models/shap_bar_top20.png` – bar plot of feature importance  
- `models/local_explanations.json` – per-sample explanations  

---

## 3️⃣ Fairness (10 marks)

Using **Fairlearn**, with **gender (sex)** as sensitive attribute:

- Compared accuracy, precision, recall, selection rate, ROC-AUC by group  
- Observed disparities:  
  - **Demographic Parity Difference:** 0.214  
  - **Equalized Odds Difference:** 0.182  

⚠️ Indicates moderate fairness concerns between male and female predictions.  

---

## 4️⃣ Dockerized API on GCP (30 marks)

- Developed **FastAPI** service with:
  - `/predict` – returns prediction + probability  
  - `/healthz` – health check  
  - `/metrics` – Prometheus metrics  

- Containerized with **Docker** (`heart-api:local`)  
- Deployed on **Google Kubernetes Engine (GKE)**:  
  - Deployment with resource requests/limits  
  - Service as LoadBalancer  
  - HPA (Horizontal Pod Autoscaler) with min=1, max=3 pods  

✅ Verified predictions through external IP and confirmed autoscaling.  

---

## 5️⃣ Logging & Observability (20 marks)

- Generated **100 synthetic rows** and sent them to the API.  
- Logged per-sample:
  - Inputs, prediction, probability, latency, timestamp  
- Saved logs in both JSONL and CSV formats.  

### Observability
- Exposed Prometheus metrics at `/metrics`:  
  - `predictions_total`  
  - `prediction_latency_seconds`  
- Verified counters and histograms before/after sending requests.  

---

## 6️⃣ Performance Monitoring & Timeout Analysis (10 marks)

Used **wrk** load testing with rotating payloads.

### Key Runs
- **c=32, t=4, 15s** → ~180 req/s baseline  
- **c=200, t=8, 60s** → 554 req/s, p50=324 ms, p99=1.02 s, 2 timeouts  
- **c=300, t=8, 60s, timeout=1s** → multiple client timeouts  

### Autoscaling
- HPA scaled pods from 1 → 3 under high load  
- Verified with `kubectl get hpa -w` and `kubectl get pods -w`  

✅ Logs in `perf/` directory with wrk outputs and screenshots.  

---

## 7️⃣ Input Drift Detection (10 marks)

### Method 1 – Statistical Tests
- **KS test** for continuous, **Chi-square** for categorical  
- Significant drift found in `oldpeak`, `cp`, `sex`  

### Method 2 – Drift Classifier
- Trained binary classifier (train=0, new=1)  
- **CV AUC = 0.73, Holdout AUC = 0.79** → moderate drift  
- Drift driven by: `oldpeak`, `thalach`, `trestbps`, `chol`, `age`, `cp`, `sex`  

✅ Outputs in `logs/` with ROC curve, feature importances, and report JSON.  

---

## 8️⃣ Data Poisoning Attack (10 marks)

Simulated **20% label flipping** (`yes ↔ no`) in training data.  

| Model      | Accuracy | Precision | Recall | AUC |
|------------|----------|-----------|--------|-----|
| Clean      | 0.84     | 0.86      | 0.82   | 0.90 |
| Poisoned   | 0.72     | 0.69      | 0.71   | 0.76 |

- Clear degradation across all metrics.  
- Plotted side-by-side bar chart (`logs/poisoning_comparison.png`).  

---

## ✅ Conclusion

This project demonstrates a **full MLOps workflow**:
- **Explainability** (SHAP)  
- **Fairness** (Fairlearn)  
- **Deployment** (Docker, FastAPI, GKE, HPA)  
- **Logging & Observability** (structured logs + Prometheus metrics)  
- **Performance Monitoring** (wrk throughput, latency, timeouts, scaling)  
- **Input Drift Detection** (statistical + model-based)  
- **Adversarial Robustness** (label-flip poisoning)  

This satisfies all rubric items and shows how to build an **explainable, fair, scalable, observable, and robust ML system in production**.

---
