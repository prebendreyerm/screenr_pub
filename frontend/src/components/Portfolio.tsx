import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

const Portfolio = () => {
  const [cash, setCash] = useState<number>(0);
  const [stocks, setStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [cashAmount, setCashAmount] = useState<number>(0);
  const [ticker, setTicker] = useState<string>("");
  const [shares, setShares] = useState<number>(0);
  const [price, setPrice] = useState<number>(0);
  const [date, setDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const [message, setMessage] = useState<string>("");
  const [loadingCash, setLoadingCash] = useState<boolean>(false);
  const [loadingStock, setLoadingStock] = useState<boolean>(false);
  const [portfolioHistory, setPortfolioHistory] = useState<any[]>([]);

  const apiUrl = "http://127.0.0.1:5000/api/portfolio/holdings"; // Adjust if needed
  const API_KEY = 'your_api_key_here'; // Add your API key

  useEffect(() => {
    const fetchPortfolioData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(apiUrl);
        setCash(response.data.cash);
        setStocks(response.data.stocks);

        // Prepare data for the chart
        const historicalData = await Promise.all(
          response.data.stocks.map(async (stock) => {
            const historicalPrices = await fetchHistoricalPrices(stock.ticker);
            return historicalPrices.map((price) => ({
              date: price.date,
              value: price.close * stock.shares,
            }));
          })
        );

        // Flatten the array and sum values by date
        const flattenedData = historicalData.flat();
        const groupedData = flattenedData.reduce((acc, entry) => {
          const existing = acc.find((item) => item.date === entry.date);
          if (existing) {
            existing.value += entry.value;
          } else {
            acc.push({ date: entry.date, value: entry.value });
          }
          return acc;
        }, []);

        setPortfolioHistory(groupedData);
      } catch (err) {
        setError("An error occurred while fetching portfolio data.");
      } finally {
        setLoading(false);
      }
    };

    const fetchHistoricalPrices = async (ticker) => {
      try {
        const response = await axios.get(`https://financialmodelingprep.com/api/v3/historical-price-full/${ticker}?apikey=${API_KEY}`);
        if (response.status === 200 && response.data.historical) {
          return response.data.historical;
        }
        throw new Error('No historical data found');
      } catch (error) {
        console.error('Error fetching historical prices:', error);
        return [];
      }
    };

    fetchPortfolioData();
  }, [apiUrl]);

  useEffect(() => {
    if (portfolioHistory.length > 0) {
      drawChart(portfolioHistory); // Draw chart when portfolioHistory changes
    }
  }, [portfolioHistory]);

  const drawChart = (history) => {
    if (window.google) {
      window.google.charts.load("current", { packages: ["corechart"] });
      window.google.charts.setOnLoadCallback(() => {
        const data = new window.google.visualization.DataTable();
        data.addColumn("string", "Date");
        data.addColumn("number", "Portfolio Value");

        history.forEach((entry) => {
          data.addRow([entry.date, entry.value]);
        });

        const options = {
          title: "Portfolio Value Over Time",
          curveType: "function",
          legend: { position: "bottom" },
        };

        const chart = new window.google.visualization.LineChart(
          document.getElementById("portfolio-chart")
        );
        chart.draw(data, options);
      });
    } else {
      console.error("Google Charts library is not loaded.");
    }
  };

  const handleCashTransaction = async (action: "deposit" | "withdraw") => {
    setLoadingCash(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/portfolio/cash", {
        amount: cashAmount,
        action,
      });
      setCash(response.data.cash);
      setCashAmount(0);
      setMessage(`Cash ${action} successful!`);
    } catch (error) {
      console.error("Error:", error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoadingCash(false);
    }
  };

  const handleStockTransaction = async (action: "buy" | "sell") => {
    setLoadingStock(true);
    try {
      await axios.post("http://127.0.0.1:5000/api/portfolio/stock", {
        ticker,
        shares,
        price,
        startDate: date,
        action,
      });

      const updatedStocks = await axios.get("http://127.0.0.1:5000/api/portfolio/holdings");
      setStocks(updatedStocks.data.stocks);

      setTicker("");
      setShares(0);
      setPrice(0);
      setDate(new Date().toISOString().split("T")[0]);
      setMessage(`Stock ${action} successful!`);
    } catch (error) {
      console.error("Error:", error);
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
          value={cashAmount === 0 ? "" : cashAmount}
          onChange={(e) => setCashAmount(e.target.value === "" ? 0 : parseFloat(e.target.value))}
        />
        <button className="btn btn-outline-light" onClick={() => handleCashTransaction("deposit")} disabled={loadingCash}>
          {loadingCash ? "Processing..." : "Deposit"}
        </button>
        <button className="btn btn-outline-light" onClick={() => handleCashTransaction("withdraw")} disabled={loadingCash}>
          {loadingCash ? "Processing..." : "Withdraw"}
        </button>
      </div>

      {/* Stock Transaction Section */}
      <div className="input-group mb-3">
        <input type="text" className="form-control bg-dark text-light" placeholder="Ticker" value={ticker} onChange={(e) => setTicker(e.target.value)} />
        <input type="number" className="form-control bg-dark text-light" placeholder="Shares" value={shares === 0 ? "" : shares} onChange={(e) => setShares(e.target.value === "" ? 0 : parseFloat(e.target.value))} />
        <input type="number" className="form-control bg-dark text-light" placeholder="Price" value={price === 0 ? "" : price} onChange={(e) => setPrice(e.target.value === "" ? 0 : parseFloat(e.target.value))} />
        <input type="date" className="form-control bg-dark text-light" value={date} onChange={(e) => setDate(e.target.value)} />
        <button className="btn btn-outline-light" onClick={() => handleStockTransaction("buy")} disabled={loadingStock}>
          {loadingStock ? "Processing..." : "Buy"}
        </button>
        <button className="btn btn-outline-light" onClick={() => handleStockTransaction("sell")} disabled={loadingStock}>
          {loadingStock ? "Processing..." : "Sell"}
        </button>
      </div>

      {/* Portfolio Value Over Time Graph */}
      <div>
        <h4>Portfolio</h4>
        <div id="portfolio-chart" style={{ width: "100%", height: "500px" }}></div>
      </div>

      {/* Portfolio Table */}
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
