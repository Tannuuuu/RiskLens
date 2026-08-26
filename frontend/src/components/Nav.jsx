import { NavLink } from "react-router-dom";

export default function Nav() {
  return (
    <header className="topnav">
      <div className="container topnav-inner">
        <NavLink to="/" className="wordmark">
          RiskLens <span className="tick">●LIVE</span>
        </NavLink>
        <nav>
          <ul className="navlinks">
            <li>
              <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
                Dashboard
              </NavLink>
            </li>
            <li>
              <NavLink to="/transactions" className={({ isActive }) => (isActive ? "active" : "")}>
                Transactions
              </NavLink>
            </li>
            <li>
              <NavLink to="/alerts" className={({ isActive }) => (isActive ? "active" : "")}>
                Alerts
              </NavLink>
            </li>
            <li>
              <NavLink to="/model" className={({ isActive }) => (isActive ? "active" : "")}>
                Model
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
