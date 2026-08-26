import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import { SkeletonRows } from "../components/Skeleton.jsx";
import RiskLabel from "../components/RiskLabel.jsx";

export default function Alerts() {
  const [alerts, setAlerts] = useState(null);
  const [filter, setFilter] = useState("open");
  const [resolvingId, setResolvingId] = useState(null);
  const [error, setError] = useState("");

  async function load() {
    setError("");
    try {
      const params = filter === "open" ? { resolved: "false" } : filter === "resolved" ? { resolved: "true" } : {};
      const data = await api.getAlerts(params);
      setAlerts(data);
    } catch (e) {
      setError(
        e.message === "Failed to fetch" ? "Can't reach the API. Is the backend running?" : e.message
      );
    }
  }

  useEffect(() => {
    setAlerts(null);
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  async function resolve(id) {
    setResolvingId(id);
    try {
      await api.resolveAlert(id, "analyst@risklens.local");
      load();
    } catch (e) {
      setError(e.message);
    } finally {
      setResolvingId(null);
    }
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">Review queue</p>
          <h1>Alerts</h1>
          <p className="lede">
            Transactions that crossed the fraud threshold land here for manual review and
            resolution.
          </p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {["open", "resolved", "all"].map((opt) => (
            <button
              key={opt}
              className="btn"
              style={filter === opt ? { borderColor: "var(--teal)", color: "var(--teal)" } : {}}
              onClick={() => setFilter(opt)}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {error && <p className="error-note" style={{ margin: "0 0 20px" }}>{error}</p>}

      <div className="panel">
        <div className="panel-body">
          <table className="ledger">
            <thead>
              <tr>
                <th>Transaction</th>
                <th>Severity</th>
                <th>Note</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {!alerts ? (
                <SkeletonRows rows={6} cols={5} />
              ) : alerts.length === 0 ? (
                <tr>
                  <td colSpan={5}>
                    <div className="empty-state">
                      <p>
                        {filter === "open"
                          ? "Nothing waiting on review right now."
                          : "No alerts match this filter yet."}
                      </p>
                    </div>
                  </td>
                </tr>
              ) : (
                alerts.map((a) => (
                  <tr key={a.id}>
                    <td className="mono">{a.transaction_id}</td>
                    <td>
                      <RiskLabel severity={a.severity} />
                    </td>
                    <td style={{ color: "var(--ink-muted)" }}>{a.message}</td>
                    <td>
                      <span className={`badge ${a.is_resolved ? "resolved" : "open"}`}>
                        {a.is_resolved ? "resolved" : "open"}
                      </span>
                    </td>
                    <td>
                      {!a.is_resolved && (
                        <button
                          className="btn"
                          disabled={resolvingId === a.id}
                          onClick={() => resolve(a.id)}
                        >
                          {resolvingId === a.id ? "Resolving…" : "Resolve"}
                        </button>
                      )}
                    </td>
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
