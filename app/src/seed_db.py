from faker import Faker
from src.database import SessionLocal, Base, engine
from src.models import User, Account, Loan
import random

fake = Faker()

def seed():
    # Reset DB each time
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    for _ in range(5):  # 5 users
        user = User(name=fake.name(), email=fake.unique.email())
        db.add(user)
        db.commit()
        db.refresh(user)

        # Each user gets 1–2 accounts
        for i in range(random.randint(1, 2)):
            account = Account(
                user_id=user.id,
                name=f"{user.name.split()[0]}'s Account {i+1}",
                balance=random.randint(100, 5000)
            )
            db.add(account)
            db.commit()
            db.refresh(account)

            # Give each account a loan
            loan = Loan(account_id=account.id, amount=random.randint(500, 5000))
            db.add(loan)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
