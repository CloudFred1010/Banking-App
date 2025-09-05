from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/")
def create_account(name: str, db: Session = Depends(get_db)):
    account = models.Account(name=name, balance=0.0)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.get("/")
def list_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()

@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    return db.query(models.Account).filter(models.Account.id == account_id).first()
