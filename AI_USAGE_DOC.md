# AI_USAGE_DOC

This document describes how **AI assistance** (ChatGPT – GPT-5) was used during the completion of the OPPE2 assignment.

---

## Scope of AI Usage

AI was used **only for support, explanation, and code drafting**, not for generating the final answers blindly. The following activities involved AI:

1. **Clarification of Concepts**
   - Understanding SHAP explainability outputs and how to phrase the insights in plain English.
   - Reviewing fairness metrics (Demographic Parity, Equalized Odds) and their interpretation.

2. **Code Drafting & Debugging**
   - Assistance in writing boilerplate code for:
     - SHAP explanations and saving plots.
     - Fairlearn `MetricFrame` usage and fixing errors related to label types.
     - FastAPI app structure and Dockerfile setup.
     - Kubernetes manifests (deployment, service, HPA).
     - Wrk load-testing scripts (`post.lua`) and parsing outputs.
     - Drift detection code (KS test, Chi-square, drift classifier).
     - Data poisoning simulation and comparison plots.
   - Debugging Python errors (e.g., type mismatches, missing dependencies in Docker).

3. **Best Practices & Guidance**
   - Suggestions on structuring logs and observability (Prometheus metrics).
   - Guidance on monitoring input drift with different methods.
   - Explanation of how autoscaling with HPA works in GKE.
   - Structuring the README for clarity and completeness.

---

## Important Notes

- **No AI-generated text was copied directly** into the final results without review.  
- All code and explanations provided by AI were **verified, adapted, and executed by me**.  
- AI was used as a **pair-programmer and explainer**, not as a replacement for actual implementation.  

---

## Declaration

This document ensures transparency regarding AI usage.  
All final outputs, logs, metrics, and deployment artifacts were **executed and validated by the author**.

---
