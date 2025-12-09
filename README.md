# 💰 Smart Expense & Budget Tracker

A full-stack smart expense and budget tracker application with FastAPI backend and React frontend. Features include transaction management, category-wise expense tracking, budget alerts, and spending insights.

## Features

✨ **Core Features:**
- 📝 Add income and expense transactions
- 📊 View expenses by category
- 💳 Budget management per category
- ⚠️ Smart budget alerts when spending exceeds 80% or 100% of limit
- 📈 Monthly summary with income, expense, and savings
- 💾 Persistent data storage with SQLite

## Tech Stack

### Backend
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Database:** SQLite
- **ORM:** Raw SQL with Python
- **API Style:** RESTful

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **HTTP Client:** Axios
- **Styling:** CSS3 with responsive design

## Project Structure

```
smart-expense-tracker/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── App.jsx              # React main component
│   └── App.css              # Styling
├── package.json             # Node.js dependencies
└── README.md                # This file
```

## Installation & Setup

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## API Endpoints

### Transactions
- `POST /transactions` - Add a new transaction
- `GET /transactions` - List all transactions
- `GET /transactions?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD` - Filter transactions by date

### Budgets
- `POST /budgets` - Set a monthly budget for a category
- `GET /budgets/alerts?month=YYYY-MM` - Get budget alerts for a specific month

### Summary
- `GET /summary?month=YYYY-MM` - Get monthly financial summary
  - Returns: total income, total expense, savings, and per-category breakdown

## Usage

1. **View Dashboard:** Open the frontend to see your financial summary for the selected month

2. **Add Transactions:**
   - Select date, amount, type (Income/Expense)
   - Choose category (Food, Transport, Rent, Shopping, etc.)
   - Add optional note
   - Click "Save Transaction"

3. **Set Budgets:** Use the API to set monthly budgets:
   ```bash
   curl -X POST http://127.0.0.1:8000/budgets \
     -H "Content-Type: application/json" \
     -d '{"month": "2025-12", "category": "Food", "limit_amount": 5000}'
   ```

4. **Monitor Alerts:** View budget alerts on the dashboard when spending exceeds limits

## Smart Features

### Budget Alerts
- Yellow alert: When spending reaches 80% of budget
- Red alert: When spending exceeds 100% of budget

### Category Breakdown
- Automatic categorization of expenses
- Monthly spending summary by category
- Visual representation of expense distribution

## Database Schema

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_date TEXT,
    amount REAL,
    tx_type TEXT,              -- INCOME or EXPENSE
    category TEXT,
    note TEXT
);
```

### Budgets Table
```sql
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT,                -- YYYY-MM format
    category TEXT,
    limit_amount REAL
);
```

## Example Workflow

1. Start both backend and frontend servers
2. Navigate to http://localhost:5173
3. Select a month to view/manage
4. Add some transactions using the form
5. Set budgets via API
6. View alerts and summaries on the dashboard
7. Monitor spending patterns over time

## Future Enhancements

- 📱 Mobile app with React Native
- 🔐 User authentication and authorization
- 📊 Advanced analytics and charts
- 💾 Data export (CSV, PDF)
- 🔔 Email notifications for budget alerts
- 🎯 Savings goals and milestones
- 🔄 Transaction editing and deletion
- 📷 Receipt scanning and OCR

## License

MIT License - Feel free to use this project for personal or educational purposes.

## Author

Created by [Your Name](https://github.com/whynotprajwal)

---

**Happy budgeting! 🎉**
