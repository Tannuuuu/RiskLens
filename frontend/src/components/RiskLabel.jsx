export function riskTier(score) {
  if (score >= 0.9) return "critical";
  if (score >= 0.7) return "high";
  if (score >= 0.5) return "medium";
  return "low";
}

export default function RiskLabel({ score, severity }) {
  const tier = severity || riskTier(score);
  return (
    <span className="risk-label">
      <span className={`risk-dot ${tier}`} />
      {tier}
    </span>
  );
}
