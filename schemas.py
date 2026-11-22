from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PatientInput(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Возраст пациента")
    systolic_bp: int = Field(..., ge=70, le=250, description="Систолическое давление")
    diastolic_bp: int = Field(..., ge=40, le=150, description="Диастолическое давление")
    heart_rate: int = Field(..., ge=30, le=220, description="Пульс")
    temperature: float = Field(..., ge=35.0, le=42.0, description="Температура тела")
    symptoms: Optional[str] = Field(None, description="Жалобы пациента")

    @model_validator(mode="after")
    def check_bp(self):
        if self.diastolic_bp >= self.systolic_bp:
            raise ValueError("diastolic_bp must be less than systolic_bp")
        return self


class PredictionResult(BaseModel):
    id: int
    patient_data: PatientInput
    risk_level: str
    recommendation: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthInfo(BaseModel):
    app: str
    version: str
    endpoints_count: int