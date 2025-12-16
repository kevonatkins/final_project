from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.auth import get_current_user
from app.models.calculation import Calculation

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def reports_summary(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
   
    total = (
        db.query(func.count(Calculation.id))
        .filter(Calculation.user_id == current_user.id)
        .scalar()
    )


    op_rows = (
        db.query(Calculation.operation, func.count(Calculation.id))
        .filter(Calculation.user_id == current_user.id)
        .group_by(Calculation.operation)
        .all()
    )
    by_operation = {op: count for op, count in op_rows}

   
    latest = (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .order_by(Calculation.created_at.desc() if hasattr(Calculation, "created_at") else Calculation.id.desc())
        .limit(5)
        .all()
    )

    latest_payload = [
        {
            "id": str(c.id),
            "operation": c.operation,
            "inputs": c.inputs,
            "result": c.result,
        }
        for c in latest
    ]

    return {
        "total": total or 0,
        "by_operation": by_operation,
        "latest": latest_payload,
    }
