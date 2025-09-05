from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_issue_card_invalid_user():
    response = client.post("/issue-card", params={"user_id": 999, "account_id": 1})
    assert response.status_code == 404

def test_repay_loan_invalid():
    response = client.post("/repay-loan", params={"loan_id": 999, "amount": 100})
    assert response.status_code == 404
