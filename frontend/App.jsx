import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [month, setMonth] = useState('2025-12');
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_URL = 'http://127.0.0.1:8000';

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const sumRes = await fetch(`${API_URL}/summary?month=${month}`);
      if (!sumRes.ok) throw new Error('Failed to fetch summary');
      const sumData = await sumRes.json();
      setSummary(sumData);

      const alertRes = await fetch(`${API_URL}/budgets/alerts?month=${month}`);
      if (!alertRes.ok) throw new Error('Failed to fetch alerts');
      const alertData = await alertRes.json();
      setAlerts(alertData.alerts || []);
    } catch (err) {
      setError(err.message);
      console.error('Error loading data:', err);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, [month]);

  const [form, setForm] = useState({
    tx_date: new Date().toISOString().slice(0, 10),
    amount: '',
    tx_type: 'EXPENSE',
    category: 'Food',
    note: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submitTx = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_URL}/transactions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          amount: parseFloat(form.amount),
        }),
      });
      if (!res.ok) throw new Error('Failed to add transaction');
      setForm({
        tx_date: new Date().toISOString().slice(0, 10),
        amount: '',
        tx_type: 'EXPENSE',
        category: 'Food',
        note: '',
      });
      loadData();
    } catch (err) {
      console.error('Error adding transaction:', err);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>💰 Smart Expense & Budget Tracker</h1>
      </header>

      {error && <div style={{ padding: '10px', background: '#ffcccb', color: 'red', marginBottom: '10px' }}>Error: {error}</div>}
      {loading && <div style={{ padding: '10px', background: '#e3f2fd', color: 'blue' }}>Loading...</div>}

      <section className="month-selector">
        <label>
          Month:
          <input
            type="month"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
          />
        </label>
      </section>

      <section className="summary-cards">
        <div className="card income">
          <h3>💵 Total Income</h3>
          <p className="amount">₹{(summary?.total_income ?? 0).toFixed(2)}</p>
        </div>
        <div className="card expense">
          <h3>💸 Total Expense</h3>
          <p className="amount">₹{(summary?.total_expense ?? 0).toFixed(2)}</p>
        </div>
        <div className="card savings">
          <h3>🎯 Savings</h3>
          <p className="amount">₹{(summary?.savings ?? 0).toFixed(2)}</p>
        </div>
      </section>

      <section className="alerts-section">
        <h2>⚠️ Budget Alerts</h2>
        {alerts.length === 0 && <p className="no-alerts">No alerts - you're doing great!</p>}
        <ul className="alerts-list">
          {alerts.map((a, i) => (
            <li key={i} className="alert-item">{a}</li>
          ))}
        </ul>
      </section>

      <section className="form-section">
        <h2>➕ Add Transaction</h2>
        <form onSubmit={submitTx} className="transaction-form">
          <div className="form-group">
            <label>Date:</label>
            <input
              type="date"
              name="tx_date"
              value={form.tx_date}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label>Amount:</label>
            <input
              type="number"
              name="amount"
              placeholder="0.00"
              value={form.amount}
              onChange={handleChange}
              step="0.01"
              required
            />
          </div>
          <div className="form-group">
            <label>Type:</label>
            <select name="tx_type" value={form.tx_type} onChange={handleChange}>
              <option value="INCOME">Income</option>
              <option value="EXPENSE">Expense</option>
            </select>
          </div>
          <div className="form-group">
            <label>Category:</label>
            <select name="category" value={form.category} onChange={handleChange}>
              <option>Food</option>
              <option>Transport</option>
              <option>Rent</option>
              <option>Shopping</option>
              <option>Entertainment</option>
              <option>Other</option>
            </select>
          </div>
          <div className="form-group">
            <label>Note:</label>
            <input
              name="note"
              placeholder="Optional note"
              value={form.note}
              onChange={handleChange}
            />
          </div>
          <button type="submit" className="submit-btn">Save Transaction</button>
        </form>
      </section>

      {summary?.per_category && (
        <section className="category-breakdown">
          <h2>📊 Expense by Category</h2>
          <div className="category-list">
            {summary.per_category.map((cat, i) => (
              <div key={i} className="category-item">
                <span className="cat-name">{cat.category}</span>
                <span className="cat-amount">₹{(cat.spent ?? 0).toFixed(2)}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default App;
