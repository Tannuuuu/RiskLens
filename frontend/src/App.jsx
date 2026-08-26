import { Routes, Route } from "react-router-dom";
import Nav from "./components/Nav.jsx";
import Footer from "./components/Footer.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Transactions from "./pages/Transactions.jsx";
import Alerts from "./pages/Alerts.jsx";
import Model from "./pages/Model.jsx";
import Privacy from "./pages/Privacy.jsx";
import Terms from "./pages/Terms.jsx";

export default function App() {
  return (
    <div className="app-shell">
      <Nav />
      <main className="page">
        <div className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/model" element={<Model />} />
            <Route path="/privacy" element={<Privacy />} />
            <Route path="/terms" element={<Terms />} />
          </Routes>
        </div>
      </main>
      <Footer />
    </div>
  );
}
