import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import axios from 'axios';

// Define the StockData interface
interface StockData {
  date: string;
  close: number;
}

interface Transaction {
  action: string; // This appears to be a date; you might want to change the name for clarity
  date: string;
  id: number;
  price: number; // Already in USD
  shares: number;
  ticker: string;
}

const Chart: React.FC = () => {
  const [chartData, setChartData] = useState<StockData[]>([]);

  useEffect(() => {
    const fetchStockPrices = async (startDate: string, endDate: string) => {
      try {
        const response = await axios.post('http://localhost:5000/api/stocks/prices', {
          ticker: 'EQNR.OL',
          startDate: startDate,
          endDate: endDate,
        });
        return response.data; // This should be your full response array
      } catch (error) {
        console.error('Error fetching stock prices:', error);
        return [];
      }
    };

    const fetchTransactions = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/portfolio/transactions');
        return response.data.transactions;
      } catch (error) {
        console.error('Error fetching transactions:', error);
        return [];
      }
    };

    const calculateCumulativePositions = (transactions: Transaction[]) => {
      const positions: { date: string; totalShares: number; totalCost: number }[] = [];
      const sharesByDate: { [key: string]: { totalShares: number; totalCost: number } } = {};

      transactions.forEach((transaction) => {
        const { date, shares, price } = transaction;
        const totalCost = shares * price;

        if (!sharesByDate[date]) {
          sharesByDate[date] = { totalShares: 0, totalCost: 0 };
        }

        sharesByDate[date].totalShares += shares;
        sharesByDate[date].totalCost += totalCost;
      });

      Object.keys(sharesByDate).forEach((date) => {
        positions.push({
          date,
          totalShares: sharesByDate[date].totalShares,
          totalCost: sharesByDate[date].totalCost,
        });
      });

      return positions;
    };

    const fetchCurrencyConversionRate = async () => {
      // Replace this with the actual endpoint or logic to fetch the conversion rate
      try {
        const response = await axios.get('http://localhost:5000/api/currency/conversion-rate');
        return response.data.rate; // Assuming the API returns an object with a 'rate' property
      } catch (error) {
        console.error('Error fetching currency conversion rate:', error);
        return 1; // Default to 1 if there's an error (no conversion)
      }
    };

    const mergeStockDataWithTransactions = (stockData: StockData[], positions: { date: string; totalShares: number; totalCost: number }[], conversionRate: number) => {
      return stockData.map((stock) => {
        const positionOnDate = positions.find((pos) => pos.date === stock.date);
        return {
          date: stock.date,
          // Convert stock close price to USD if it's not already (assuming it's in local currency)
          close: positionOnDate && positionOnDate.totalShares > 0
            ? (positionOnDate.totalCost / positionOnDate.totalShares)
            : stock.close * conversionRate, // Convert to USD using the conversion rate
        };
      });
    };

    const startDate = '2024-01-01';
    const endDate = '2024-10-18';

    const fetchData = async () => {
      const stockData = await fetchStockPrices(startDate, endDate);
      const transactions = await fetchTransactions();
      const positions = calculateCumulativePositions(transactions);

      // Sort the stockData and positions by date in ascending order
      const sortedStockData = stockData.sort((a: StockData, b: StockData) => new Date(a.date).getTime() - new Date(b.date).getTime());
      const sortedPositions = positions.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

      const conversionRate = await fetchCurrencyConversionRate(); // Fetch the conversion rate
      const mergedData = mergeStockDataWithTransactions(sortedStockData, sortedPositions, conversionRate); // Pass the conversion rate
      setChartData(mergedData);
    };

    fetchData();
  }, []);

  return (
    <div className="chart-container">
      <h1>EQNR.OL Stock Price Development</h1>

      {/* Render the chart */}
      {chartData.length === 0 ? (
        <p>No data to display</p>
      ) : (
        <LineChart
          width={window.innerWidth * 0.95}  // Full width of the window
          height={window.innerHeight * 0.8} // 80% of the window height
          data={chartData}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} />
        </LineChart>
      )}
    </div>
  );
};

export default Chart;
