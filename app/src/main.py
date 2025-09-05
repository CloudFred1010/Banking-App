from fastapi import FastAPI
from src.database import engine, Base
from src.routes import accounts, transactions, loans

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Banking Demo API is running"}

# 🔹 Healthcheck endpoint for container probes
@app.get("/health")
def health():
    return {"status": "ok"}

# Register routers
app.include_router(accounts.router)
app.include_router(transactions.router)
app.include_router(loans.router)
