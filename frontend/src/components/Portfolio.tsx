import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

const Portfolio = () => {
  const [cash, setCash] = useState<number>(0);
  const [stocks, setStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [cashAmount, setCashAmount] = useState<number>(0);
  const [ticker, setTicker] = useState<string>('');
  const [shares, setShares] = useState<number>(0);
  const [price, setPrice] = useState<number>(0); // Add price state
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0]); // Default to today's date
  const [message, setMessage] = useState<string>('');
  const [loadingCash, setLoadingCash] = useState<boolean>(false);
  const [loadingStock, setLoadingStock] = useState<boolean>(false);

  const apiUrl = 'http://127.0.0.1:5000/api/portfolio/holdings'; // Adjust if needed

  useEffect(() => {
    const fetchPortfolioData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(apiUrl);
        setCash(response.data.cash);
        setStocks(response.data.stocks);
      } catch (err) {
        setError('An error occurred while fetching portfolio data.');
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolioData();
  }, [apiUrl]);

  const handleCashTransaction = async (action: 'deposit' | 'withdraw') => {
    setLoadingCash(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/portfolio/cash', {
        amount: cashAmount,
        action,
      });
      setCash(response.data.cash); // Update the cash state with the returned cash value
      setCashAmount(0);
      setMessage(`Cash ${action} successful!`);
    } catch (error) {
      console.error('Error:', error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoadingCash(false);
    }
  };

  const handleStockTransaction = async (action: 'buy' | 'sell') => {
    setLoadingStock(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/portfolio/stock', {
        ticker,
        shares,
        price, // Send price as part of the transaction
        startDate: date, // Ensure startDate is sent
        action,
      });

      // Ensure the state is updated with the latest data returned from the API
      const updatedStocks = await axios.get('http://127.0.0.1:5000/api/portfolio/holdings');
      setStocks(updatedStocks.data.stocks);

      // Clear form fields after successful transaction
      setTicker('');
      setShares(0);
      setPrice(0); // Clear price input
      setDate(new Date().toISOString().split('T')[0]); // Reset date to today's date
      setMessage(`Stock ${action} successful!`);
    } catch (error) {
      console.error('Error:', error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoadingStock(false);
    }
  };

  if (loading) return <div className="spinner-border" role="status"></div>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Portfolio Holdings</h2>
      <h4>Cash: ${cash.toFixed(2)}</h4>
      {message && <div className="alert alert-info">{message}</div>}

      {/* Cash Transaction Section */}
      <div className="input-group mb-3">
        <input 
          type="number" 
          className="form-control bg-dark text-light" 
          placeholder="Amount" 
          value={cashAmount === 0 ? '' : cashAmount}
          onChange={(e) => setCashAmount(e.target.value === '' ? 0 : parseFloat(e.target.value))}
        />
        <button 
          className="btn btn-outline-light"
          onClick={() => handleCashTransaction('deposit')}
          disabled={loadingCash}
        >
          {loadingCash ? 'Processing...' : 'Deposit'}
        </button>
        <button 
          className="btn btn-outline-light"
          onClick={() => handleCashTransaction('withdraw')}
          disabled={loadingCash}
        >
          {loadingCash ? 'Processing...' : 'Withdraw'}
        </button>
      </div>

      {/* Stock Transaction Section */}
      <div className="input-group mb-3">
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
          value={shares === 0 ? '' : shares}
          onChange={(e) => setShares(e.target.value === '' ? 0 : parseInt(e.target.value, 10))}
        />
        <input 
          type="number" 
          className="form-control bg-dark text-light" 
          placeholder="Price" 
          value={price === 0 ? '' : price} // Price input
          onChange={(e) => setPrice(e.target.value === '' ? 0 : parseFloat(e.target.value))}
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
          disabled={loadingStock}
        >
          {loadingStock ? 'Processing...' : 'Buy'}
        </button>
        <button 
          className="btn btn-outline-light"
          onClick={() => handleStockTransaction('sell')}
          disabled={loadingStock}
        >
          {loadingStock ? 'Processing...' : 'Sell'}
        </button>
      </div>

      {stocks.length === 0 ? (
        <p>No stocks in your portfolio.</p>
      ) : (
        <table className="table table-dark">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Shares</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock, index) => (
              <tr key={index}>
                <td>{stock.ticker}</td>
                <td>{stock.shares}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Portfolio;
