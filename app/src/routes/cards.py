from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Card, Account, User
import random

router = APIRouter()

@router.post("/issue-card")
def issue_card(user_id: int, account_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    account = db.query(Account).filter(Account.id == account_id).first()
    if not user or not account:
        raise HTTPException(status_code=404, detail="User or account not found")

    card_number = str(random.randint(10**15, (10**16)-1))  # 16-digit card
    card = Card(card_number=card_number, expiry="12/30", user_id=user.id, account_id=account.id)
    db.add(card)
    db.commit()
    db.refresh(card)
    return {"message": "Card issued", "card_number": card.card_number}
