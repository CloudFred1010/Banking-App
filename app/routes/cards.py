from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
import random

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/{account_id}/issue")
def issue_card(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        return {"error": "Account not found"}

    card_number = str(random.randint(4000000000000000, 4999999999999999))  # pseudo Visa #
    card = models.Card(account_id=account_id, card_number=card_number)
    db.add(card)
    db.commit()
    db.refresh(card)
    return {"message": "Card issued", "card_number": card.card_number}
