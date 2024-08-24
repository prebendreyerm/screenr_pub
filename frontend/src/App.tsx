import React from 'react';
import StockTable from './components/StockTable';
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
    { key: 'enterpriseValueMultipleTTM', label: 'EV Multiple' }
  ];

  return (
    <div className="App text-bg-dark">
      <h1 className="mb-4">Screenr</h1>
      <StockTable apiUrl={apiUrl} columns={columns} />
    </div>
  );
};

export default App;
