from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import List, Optional
import sqlite3

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect("expense.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_date TEXT,
            amount REAL,
            tx_type TEXT,
            category TEXT,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            category TEXT,
            limit_amount REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class TransactionIn(BaseModel):
    tx_date: date
    amount: float
    tx_type: str
    category: str
    note: Optional[str] = ""

class BudgetIn(BaseModel):
    month: str
    category: str
    limit_amount: float

@app.post("/transactions")
def add_transaction(tx: TransactionIn):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions(tx_date, amount, tx_type, category, note) VALUES (?,?,?,?,?)",
        (tx.tx_date.isoformat(), tx.amount, tx.tx_type, tx.category, tx.note),
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/transactions")
def list_transactions(from_date: Optional[date] = None, to_date: Optional[date] = None):
    conn = get_db()
    cur = conn.cursor()
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    if from_date:
        query += " AND tx_date >= ?"
        params.append(from_date.isoformat())
    if to_date:
        query += " AND tx_date <= ?"
        params.append(to_date.isoformat())
    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.post("/budgets")
def set_budget(b: BudgetIn):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM budgets WHERE month = ? AND category = ?",
        (b.month, b.category),
    )
    cur.execute(
        "INSERT INTO budgets(month, category, limit_amount) VALUES (?,?,?)",
        (b.month, b.category, b.limit_amount),
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/summary")
def summary(month: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
          SUM(CASE WHEN tx_type='INCOME' THEN amount ELSE 0 END) as total_income,
          SUM(CASE WHEN tx_type='EXPENSE' THEN amount ELSE 0 END) as total_expense
        FROM transactions
        WHERE substr(tx_date,1,7) = ?
        """,
        (month,),
    )
    totals = cur.fetchone()
    cur.execute(
        """
        SELECT category,
               SUM(CASE WHEN tx_type='EXPENSE' THEN amount ELSE 0 END) as spent
        FROM transactions
        WHERE substr(tx_date,1,7) = ?
        GROUP BY category
        """,
        (month,),
    )
    per_cat = [dict(r) for r in cur.fetchall()]
    conn.close()
    total_income = totals["total_income"] or 0
    total_expense = totals["total_expense"] or 0
    return {
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": total_income - total_expense,
        "per_category": per_cat,
    }

@app.get("/budgets/alerts")
def budget_alerts(month: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT category, limit_amount FROM budgets WHERE month = ?", (month,))
    budgets = [dict(r) for r in cur.fetchall()]
    alerts = []
    for b in budgets:
        cur.execute(
            """
            SELECT SUM(amount) as spent
            FROM transactions
            WHERE tx_type='EXPENSE'
              AND category = ?
              AND substr(tx_date,1,7) = ?
            """,
            (b["category"], month),
        )
        row = cur.fetchone()
        spent = row["spent"] or 0
        ratio = spent / b["limit_amount"] if b["limit_amount"] > 0 else 0
        if ratio >= 1:
            alerts.append(f"Over budget in {b['category']} (spent {spent}).")
        elif ratio >= 0.8:
            alerts.append(f"Warning: {b['category']} budget at {int(ratio*100)}%.")
    conn.close()
    return {"alerts": alerts}

@app.get("/")
def root():
    return {"message": "Smart Expense Tracker API"}
