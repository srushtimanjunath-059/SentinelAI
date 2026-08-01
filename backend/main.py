from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base, Transaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "project": "Sentinel AI",
        "status": "Running"
    }

@app.get("/analyze/{amount}")
def analyze(amount: int):

    risk = 10

    if amount > 10000:
        risk += 20

    if amount > 50000:
        risk += 30

    if amount > 100000:
        risk += 30

    db = SessionLocal()

    transaction = Transaction(
        amount=amount,
        risk_score=risk
    )

    db.add(transaction)
    db.commit()
    db.close()

    return {
        "amount": amount,
        "risk_score": risk
    }
@app.get("/transactions")
def get_transactions():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    result = []

    for t in transactions:
        result.append({
            "id": t.id,
            "amount": t.amount,
            "risk_score": t.risk_score
        })

    db.close()

    return result