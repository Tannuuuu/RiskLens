import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import { SkeletonRows } from "../components/Skeleton.jsx";
import RiskLabel from "../components/RiskLabel.jsx";

const emptyForm = {
  amount: "",
  card_number: "4242424242424242",
  merchant_id: "",
  merchant_category: "",
  location: "",
};

export default function Transactions() {
  const [transactions, setTransactions] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loadError, setLoadError] = useState("");

  async function load() {
    setLoadError("");
    try {
      const data = await api.getTransactions(0, 100);
      setTransactions(data);
    } catch (e) {
      setLoadError(
        e.message === "Failed to fetch" ? "Can't reach the API. Is the backend running?" : e.message
      );
    }
  }

  useEffect(() => {
    load();
  }, []);

  function updateField(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);
    try {
      const payload = {
        amount: parseFloat(form.amount),
        card_number: form.card_number,
        merchant_id: form.merchant_id,
        merchant_category: form.merchant_category || null,
        location: form.location || null,
      };
      const result = await api.createTransaction(payload);
      setSuccess(`Logged ${result.transaction_id}, scored ${result.fraud_score.toFixed(3)}.`);
      setForm(emptyForm);
      load();
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">Ledger</p>
          <h1>Transactions</h1>
          <p className="lede">
            Log a transaction to see it scored against the trained Isolation Forest model in
            real time.
          </p>
        </div>
      </div>

      <div className="panel">
        <div className="panel-head">
          <h2>Log a transaction</h2>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="field">
              <label htmlFor="amount">Amount (USD)</label>
              <input
                id="amount"
                type="number"
                step="0.01"
                min="0.01"
                required
                value={form.amount}
                onChange={(e) => updateField("amount", e.target.value)}
                placeholder="128.50"
              />
            </div>
            <div className="field">
              <label htmlFor="card">Card number</label>
              <input
                id="card"
                required
                minLength={16}
                maxLength={19}
                value={form.card_number}
                onChange={(e) => updateField("card_number", e.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="merchant">Merchant ID</label>
              <input
                id="merchant"
                required
                value={form.merchant_id}
                onChange={(e) => updateField("merchant_id", e.target.value)}
                placeholder="MERCH-0091"
              />
            </div>
            <div className="field">
              <label htmlFor="category">Category</label>
              <input
                id="category"
                value={form.merchant_category}
                onChange={(e) => updateField("merchant_category", e.target.value)}
                placeholder="electronics"
              />
            </div>
            <div className="field">
              <label htmlFor="location">Location</label>
              <input
                id="location"
                value={form.location}
                onChange={(e) => updateField("location", e.target.value)}
                placeholder="Newark, NJ"
              />
            </div>
          </div>
          {error && <p className="error-note">{error}</p>}
          {success && <p className="success-note">{success}</p>}
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? "Scoring…" : "Submit transaction"}
            </button>
            <span style={{ fontSize: 12.5, color: "var(--ink-muted)" }}>
              Card numbers here are test values only. Nothing is charged.
            </span>
          </div>
        </form>
      </div>

      <div className="panel">
        <div className="panel-head">
          <h2>All transactions</h2>
        </div>
        <div className="panel-body">
          <table className="ledger">
            <thead>
              <tr>
                <th>Transaction</th>
                <th>Merchant</th>
                <th>Category</th>
                <th>Location</th>
                <th>Risk</th>
                <th className="amount">Amount</th>
              </tr>
            </thead>
            <tbody>
              {loadError ? (
                <tr>
                  <td colSpan={6}>
                    <div className="empty-state">
                      <p>{loadError}</p>
                    </div>
                  </td>
                </tr>
              ) : !transactions ? (
                <SkeletonRows rows={8} cols={6} />
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={6}>
                    <div className="empty-state">
                      <p>No transactions logged yet. Use the form above to add the first one.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                transactions.map((t) => (
                  <tr key={t.id}>
                    <td className="mono">{t.transaction_id}</td>
                    <td>{t.merchant_id}</td>
                    <td>{t.merchant_category || "—"}</td>
                    <td>{t.location || "—"}</td>
                    <td>
                      <RiskLabel score={t.fraud_score} />
                    </td>
                    <td className="amount">${t.amount.toFixed(2)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
