import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import axios from 'axios';

// Define the StockData interface
interface StockData {
  date: string;
  close: number; // Close price in local currency (NOK)
}

// Define the Transaction interface
interface Transaction {
  action: string;
  date: string;
  shares: number;
  price: number;
  ticker: string;
}

const Chart: React.FC = () => {
  const [chartData, setChartData] = useState<StockData[]>([]);
  const [totalHoldings, setTotalHoldings] = useState<any[]>([]); // State for total holdings values

  useEffect(() => {
    const fetchStockPrices = async (startDate: string, endDate: string) => {
      try {
        const response = await axios.post('http://localhost:5000/api/stocks/prices', {
          ticker: 'EQNR.OL',
          startDate: startDate,
          endDate: endDate,
        });
        console.log('Stock Data:', response.data); // Log stock data
        return response.data; // This should be your full response array
      } catch (error) {
        console.error('Error fetching stock prices:', error);
        return [];
      }
    };

    const fetchTransactions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/portfolio/transactions');
        console.log('Transactions Data:', response.data); // Log transactions data
        return response.data.transactions; // Assuming the response has a 'transactions' property
      } catch (error) {
        console.error('Error fetching transactions:', error);
        return [];
      }
    };

    const fetchData = async () => {
      const startDate = '2022-09-19'; // Start date to align with the earliest transaction
      const endDate = '2024-10-18';

      const stockData = await fetchStockPrices(startDate, endDate);
      const transactions = await fetchTransactions();

      // Sort transactions by date to apply them in the correct order
      transactions.sort((a: Transaction, b: Transaction) => new Date(a.date).getTime() - new Date(b.date).getTime());

      // Initialize holdings for EQNR.OL
      let totalShares = 0;
      let firstBuyFound = false;
      const totalHoldingsValues: any[] = [];

      // Iterate over the stock data
      stockData.forEach(stock => {
        // For each stock date, apply transactions that occurred before or on that date
        transactions.forEach(transaction => {
          if (transaction.ticker === 'EQNR.OL' && new Date(transaction.date) <= new Date(stock.date)) {
            if (transaction.action === 'buy') {
              totalShares += transaction.shares;
              firstBuyFound = true;
            }
            if (transaction.action === 'sell') {
              totalShares -= transaction.shares; // Deduct shares on sell action
            }
          }
        });

        // Calculate total value of holdings on the current stock date, but only if the first buy has occurred
        const totalValue = totalShares * stock.close;
          totalHoldingsValues.push({
            date: stock.date,
            totalValue,
          });

        // Reset firstBuyFound for the next day
        firstBuyFound = false;
      });

      // Sort total holdings values by date to ensure they match stock data
      totalHoldingsValues.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

      console.log('Total Holdings Values:', totalHoldingsValues); // Log total holdings values

      setTotalHoldings(totalHoldingsValues); // Save total holdings to state
      setChartData(stockData); // Set stock data for the chart
    };

    fetchData();
  }, []);

  return (
    <div className="chart-container">
      <h1>EQNR.OL Stock Price Development</h1>

      {/* Render the chart */}
      {chartData.length === 0 || totalHoldings.length === 0 ? (
        <p>No data to display</p>
      ) : (
        <LineChart
          width={window.innerWidth * 0.95}  // Full width of the window
          height={window.innerHeight * 0.8} // 80% of the window height
          data={totalHoldings} // Use total holdings for the chart
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="totalValue" stroke="#8884d8" dot={false} />
        </LineChart>
      )}
    </div>
  );
};

export default Chart;