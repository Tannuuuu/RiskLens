import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <span>RiskLens, a transaction monitoring ledger.</span>
        <span>
          <Link to="/privacy">Privacy policy</Link>
          <Link to="/terms">Terms of service</Link>
        </span>
      </div>
    </footer>
  );
}
