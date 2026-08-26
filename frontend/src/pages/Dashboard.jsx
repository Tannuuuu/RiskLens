import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../services/api.js";
import { SkeletonStatStrip, SkeletonRows } from "../components/Skeleton.jsx";
import RiskLabel from "../components/RiskLabel.jsx";

function pct(n) {
  return `${(n * 100).toFixed(2)}%`;
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [transactions, setTransactions] = useState(null);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      const [statsData, txnData] = await Promise.all([
        api.getDashboardStats(),
        api.getTransactions(0, 8),
      ]);
      setStats(statsData);
      setTransactions(txnData);
    } catch (e) {
      setError(
        e.message === "Failed to fetch"
          ? "Can't reach the API. Is the backend running?"
          : e.message
      );
    }
  }

  useEffect(() => {
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">Overview</p>
          <h1>Monitoring ledger</h1>
          <p className="lede">
            Every transaction is scored the moment it lands. Flagged activity moves to the alert
            queue for review.
          </p>
        </div>
        <Link to="/transactions" className="btn btn-primary">
          Log a transaction
        </Link>
      </div>

      {error && <p className="error-note" style={{ margin: "0 0 20px" }}>{error}</p>}

      {!stats ? (
        <SkeletonStatStrip count={5} />
      ) : (
        <div className="stat-strip">
          <div className="stat-cell">
            <p className="label">Transactions</p>
            <p className="value">{stats.total_transactions.toLocaleString()}</p>
          </div>
          <div className="stat-cell">
            <p className="label">Flagged fraud</p>
            <p className="value">{stats.total_fraud.toLocaleString()}</p>
          </div>
          <div className="stat-cell">
            <p className="label">Fraud rate</p>
            <p className="value">{pct(stats.fraud_rate)}</p>
          </div>
          <div className="stat-cell">
            <p className="label">Alerts open</p>
            <p className="value warn">{stats.unresolved_alerts}</p>
          </div>
          <div className="stat-cell">
            <p className="label">Alerts total</p>
            <p className="value">{stats.total_alerts}</p>
          </div>
        </div>
      )}

      <div className="panel">
        <div className="panel-head">
          <h2>Recent activity</h2>
          <Link to="/transactions" className="btn">
            View all
          </Link>
        </div>
        <div className="panel-body">
          <table className="ledger">
            <thead>
              <tr>
                <th>Transaction</th>
                <th>Merchant</th>
                <th>Risk</th>
                <th className="amount">Amount</th>
              </tr>
            </thead>
            <tbody>
              {!transactions ? (
                <SkeletonRows rows={6} cols={4} />
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={4}>
                    <div className="empty-state">
                      <p>Nothing logged yet. Once transactions come in, they'll show up here.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                transactions.map((t) => (
                  <tr key={t.id}>
                    <td className="mono">{t.transaction_id}</td>
                    <td>{t.merchant_id}</td>
                    <td>
                      <RiskLabel score={t.fraud_score} />
                      <span className="score-bar">
                        <span
                          className="score-bar-fill"
                          style={{ width: `${Math.min(t.fraud_score * 100, 100)}%` }}
                        />
                      </span>
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
