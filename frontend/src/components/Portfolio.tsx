import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

const Portfolio = () => {
  const [cashAmount, setCashAmount] = useState(0);
  const [ticker, setTicker] = useState('');
  const [shares, setShares] = useState(0);
  const [cost, setCost] = useState(0);
  const [date, setDate] = useState('');

  const handleCashTransaction = (action) => {
    fetch('/api/portfolio/cash', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: cashAmount,
        action,
      }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  };

  const handleStockTransaction = (action) => {
    fetch('/api/portfolio/stock', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ticker,
        shares,
        cost,
        date,
        action,
      }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  };

  return (
    <div className="container">
      <div className="row justify-content-left">
        <div className="col-12 col-md-4 mb-3">
          <div className="input-group">
            <span className="input-group-text bg-dark text-light">Cash</span>
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Amount" 
              value={cashAmount} 
              onChange={(e) => setCashAmount(e.target.value)}
            />
            <button
              className="btn btn-outline-light"
              onClick={() => handleCashTransaction('deposit')}
            >Deposit</button>
            <button
              className="btn btn-outline-light"
              onClick={() => handleCashTransaction('withdraw')}
            >Withdraw</button>
          </div>
        </div>
      </div>

      <div className="row justify-content-left">
        <div className="col-12 col-md-7 mb-3">
          <div className="input-group mb-2">
            <span className="input-group-text bg-dark text-light">Stock</span>
            <input 
              type="text" 
              className="form-control bg-dark text-light" 
              placeholder="Ticker" 
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
            />
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Shares" 
              value={shares}
              onChange={(e) => setShares(e.target.value)}
            />
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Cost" 
              value={cost}
              onChange={(e) => setCost(e.target.value)}
            />
            <input 
              type="date" 
              className="form-control bg-dark text-light"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <button
              className="btn btn-outline-light"
              onClick={() => handleStockTransaction('buy')}
            >Buy</button>
            <button
              className="btn btn-outline-light"
              onClick={() => handleStockTransaction('sell')}
            >Sell</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
