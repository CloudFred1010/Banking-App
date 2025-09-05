from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/{account_id}/deposit")
def deposit(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    account.balance += amount
    txn = models.Transaction(account_id=account_id, amount=amount, type="deposit")
    db.add(txn)
    db.commit()
    db.refresh(account)
    return {"message": "Deposit successful", "new_balance": account.balance}

@router.post("/{account_id}/withdraw")
def withdraw(account_id: int, amount: float, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if account.balance < amount:
        return {"error": "Insufficient funds"}
    account.balance -= amount
    txn = models.Transaction(account_id=account_id, amount=amount, type="withdrawal")
    db.add(txn)
    db.commit()
    db.refresh(account)
    return {"message": "Withdrawal successful", "new_balance": account.balance}
