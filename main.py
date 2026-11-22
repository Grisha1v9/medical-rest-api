from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from crud import delete_result, get_all_results, get_result_by_id, save_result
from database import Base, ResultRecord, engine, get_db
from langgraph_agent import run_agent
from schemas import HealthInfo, PatientInput, PredictionResult


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Medical REST API",
    description="REST API для медицинского приложения с обработкой через LangGraph",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/predict", response_model=PredictionResult, tags=["prediction"])
def predict(data: PatientInput, db: Session = Depends(get_db)):
    """Принять данные пациента и вернуть результат обработки (LangGraph)."""
    result = run_agent(data.model_dump())
    record = save_result(db, data, result["risk_level"], result["recommendation"])
    return _to_response(record)


@app.get("/results", response_model=list[PredictionResult], tags=["results"])
def list_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех результатов."""
    return [_to_response(r) for r in get_all_results(db, skip, limit)]


@app.get("/results/{result_id}", response_model=PredictionResult, tags=["results"])
def get_result(result_id: int, db: Session = Depends(get_db)):
    """Получить результат по ID."""
    record = get_result_by_id(db, result_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Result {result_id} not found")
    return _to_response(record)


@app.delete("/results/{result_id}", tags=["results"])
def remove_result(result_id: int, db: Session = Depends(get_db)):
    """Удалить результат по ID."""
    record = delete_result(db, result_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Result {result_id} not found")
    return {"detail": "deleted", "id": result_id}


@app.get("/health", response_model=HealthInfo, tags=["service"])
def health():
    """Служебная информация о приложении."""
    return {"app": "Medical REST API", "version": "1.0.0", "endpoints_count": 5}


def _to_response(record: ResultRecord) -> dict:
    return {
        "id": record.id,
        "patient_data": {
            "age": record.age,
            "systolic_bp": record.systolic_bp,
            "diastolic_bp": record.diastolic_bp,
            "heart_rate": record.heart_rate,
            "temperature": record.temperature,
            "symptoms": record.symptoms,
        },
        "risk_level": record.risk_level,
        "recommendation": record.recommendation,
        "created_at": record.created_at,
    }