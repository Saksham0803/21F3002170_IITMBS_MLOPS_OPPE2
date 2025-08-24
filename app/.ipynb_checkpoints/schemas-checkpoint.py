from pydantic import BaseModel, Field

class HeartRequest(BaseModel):
    # Adjust fields to your dataset columns (order must match training X)
    age: int
    sex: int = Field(..., description="0=female, 1=male")
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

class HeartResponse(BaseModel):
    prediction: int
    probability: float
