import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import StockTable from './components/StockTable'; // Make sure this path is correct
import Home from './components/Home'; // Import Home component
import About from './components/About'; // Import About component
import Portfolio from './components/Portfolio';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import './App.css';

const App: React.FC = () => {
  const apiUrl = 'http://localhost:5000/api/stocks/scores';
  const columns = [
    { key: 'name', label: 'Company Name' },
    { key: 'symbol', label: 'Ticker' },
    { key: 'sector', label: 'Sector' },
    { key: 'exchangeShortName', label: 'Exchange' },
    { key: 'score', label: 'Score' },
    { key: 'enterpriseValueMultipleTTM', label: 'EV Multiple' },
  ];

  return (
    <Router>
      <div className="App text-bg-dark">
        {/* Bootstrap Navbar */}
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">Screenr</Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/stocks">Screener</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/portfolio">Portfolio</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/about">About</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stocks" element={<StockTable apiUrl={apiUrl} columns={columns} />} />
          <Route path="/about" element={<About />} />
          <Route path="/portfolio" element={<Portfolio />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
