@router.post("/{loan_id}/repay")
def repay_loan(loan_id: int, amount: float, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan:
        return {"error": "Loan not found"}
    if loan.status != "approved":
        return {"error": "Loan is not approved"}

    account = db.query(models.Account).filter(models.Account.id == loan.account_id).first()
    if not account or account.balance < amount:
        return {"error": "Insufficient funds to repay loan"}

    account.balance -= amount
    db.commit()
    return {"message": "Loan repayment successful", "remaining_balance": account.balance}
