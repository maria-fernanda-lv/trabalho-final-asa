from sqlalchemy.orm import Session
from fastapi import HTTPException

def validate_foreign_key(db: Session, model, record_id: int):
    
    record = db.query(model).filter(model.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id {record_id} not found.")
    return record
