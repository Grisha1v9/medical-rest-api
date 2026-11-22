from sqlalchemy.orm import Session

from database import ResultRecord
from schemas import PatientInput


def save_result(db: Session, data: PatientInput, risk: str, rec: str) -> ResultRecord:
    record = ResultRecord(
        age=data.age, systolic_bp=data.systolic_bp, diastolic_bp=data.diastolic_bp,
        heart_rate=data.heart_rate, temperature=data.temperature, symptoms=data.symptoms,
        risk_level=risk, recommendation=rec,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_all_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ResultRecord).offset(skip).limit(limit).all()


def get_result_by_id(db: Session, result_id: int):
    return db.query(ResultRecord).filter(ResultRecord.id == result_id).first()


def delete_result(db: Session, result_id: int):
    record = db.query(ResultRecord).filter(ResultRecord.id == result_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record