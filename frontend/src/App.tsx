import React from 'react';
import StockTable from './components/StockTable';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App: React.FC = () => {
  const apiUrl = 'http://localhost:5000/api/stocks/scores';
  const columns = [
    { key: 'name', label: 'Company Name' },
    { key: 'symbol', label: 'Ticker' },
    { key: 'sector', label: 'Sector' },
    { key: 'exchangeShortName', label: 'Exchange' },
    { key: 'score', label: 'Score' },
    { key: 'enterpriseValueMultipleTTM', label: 'EV Multiple' }
  ];

  return (
    <div className="App text-bg-dark">
      <h1 className="mb-4">Screenr</h1>
      <div className="d-flex justify-content-start mb-3">
        <div className="dropdown">
          <button
            className="btn btn-primary btn-sm dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Strategy
          </button>
          <ul className="dropdown-menu">
            <li><a className="dropdown-item" href="#">Option 1</a></li>
            <li><a className="dropdown-item" href="#">Option 2</a></li>
            <li><a className="dropdown-item" href="#">Option 3</a></li>
          </ul>
        </div>
      </div>
      <StockTable apiUrl={apiUrl} columns={columns} />
    </div>
  );
};

export default App;
