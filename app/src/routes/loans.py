from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/loans", tags=["Loans"])  # <-- must exist before decorators

@router.post("/{account_id}/apply")
def apply_loan(account_id: int, amount: float, db: Session = Depends(get_db)):
    loan = models.Loan(account_id=account_id, amount=amount)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return {"message": "Loan application submitted", "loan_id": loan.id, "status": loan.status}

@router.post("/{loan_id}/approve")
def approve_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    loan.status = "approved"
    db.commit()
    return {"message": "Loan approved", "loan_id": loan.id}

@router.post("/{loan_id}/reject")
def reject_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    loan.status = "rejected"
    db.commit()
    return {"message": "Loan rejected", "loan_id": loan.id}

@router.post("/{loan_id}/repay-loan")
def repay_loan(loan_id: int, amount: float, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if loan.status != "approved":
        return {"error": "Only approved loans can be repaid"}
    account = db.query(models.Account).filter(models.Account.id == loan.account_id).first()
    if account.balance < amount:
        return {"error": "Insufficient funds"}
    account.balance -= amount
    db.commit()
    return {"message": "Loan repayment successful", "remaining_balance": account.balance}
