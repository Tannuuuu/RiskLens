const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || detail;
    } catch {
      // response wasn't JSON, keep default detail
    }
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  getDashboardStats: () => request("/dashboard/stats"),
  getTransactions: (skip = 0, limit = 50) => request(`/transactions?skip=${skip}&limit=${limit}`),
  getTransaction: (id) => request(`/transactions/${id}`),
  createTransaction: (payload) =>
    request("/transactions", { method: "POST", body: JSON.stringify(payload) }),
  getAlerts: (params = {}) => {
    const query = new URLSearchParams(params).toString();
    return request(`/alerts${query ? `?${query}` : ""}`);
  },
  resolveAlert: (id, resolvedBy) =>
    request(`/alerts/${id}/resolve`, {
      method: "PUT",
      body: JSON.stringify({ resolved_by: resolvedBy }),
    }),
  getModelMetrics: () => request("/model/metrics"),
  trainModel: (dataPath) =>
    request("/model/train", { method: "POST", body: JSON.stringify({ data_path: dataPath }) }),
};
