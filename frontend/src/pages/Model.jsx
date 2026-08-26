import { useEffect, useState } from "react";
import { api } from "../services/api.js";
import { SkeletonRows } from "../components/Skeleton.jsx";

function fmt(n) {
  return n === null || n === undefined ? "—" : n.toFixed(3);
}

export default function Model() {
  const [metrics, setMetrics] = useState(null);
  const [training, setTraining] = useState(false);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");

  async function load() {
    setError("");
    try {
      const data = await api.getModelMetrics();
      setMetrics(data);
    } catch (e) {
      setError(
        e.message === "Failed to fetch" ? "Can't reach the API. Is the backend running?" : e.message
      );
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleTrain() {
    setTraining(true);
    setNote("");
    setError("");
    try {
      const result = await api.trainModel("data/creditcard.csv");
      setNote(result.message);
      load();
    } catch (e) {
      setError(e.message);
    } finally {
      setTraining(false);
    }
  }

  return (
    <>
      <div className="page-head">
        <div>
          <p className="eyebrow">Isolation forest</p>
          <h1>Model</h1>
          <p className="lede">
            Retrain against the dataset on disk and track how precision and recall move across
            versions.
          </p>
        </div>
        <button className="btn btn-primary" onClick={handleTrain} disabled={training}>
          {training ? "Training…" : "Retrain model"}
        </button>
      </div>

      {error && <p className="error-note" style={{ margin: "0 0 20px" }}>{error}</p>}
      {note && <p className="success-note" style={{ margin: "0 0 20px" }}>{note}</p>}

      <div className="panel">
        <div className="panel-head">
          <h2>Training history</h2>
        </div>
        <div className="panel-body">
          <table className="ledger">
            <thead>
              <tr>
                <th>Version</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1</th>
                <th>AUC-ROC</th>
                <th className="amount">Samples</th>
              </tr>
            </thead>
            <tbody>
              {!metrics ? (
                <SkeletonRows rows={4} cols={6} />
              ) : metrics.length === 0 ? (
                <tr>
                  <td colSpan={6}>
                    <div className="empty-state">
                      <p>No trained versions yet. Run the training script or use the button above.</p>
                    </div>
                  </td>
                </tr>
              ) : (
                metrics.map((m) => (
                  <tr key={m.id}>
                    <td className="mono">{m.model_version}</td>
                    <td className="mono">{fmt(m.precision_score)}</td>
                    <td className="mono">{fmt(m.recall_score)}</td>
                    <td className="mono">{fmt(m.f1_score)}</td>
                    <td className="mono">{fmt(m.auc_roc)}</td>
                    <td className="amount">{m.training_samples?.toLocaleString() || "—"}</td>
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
