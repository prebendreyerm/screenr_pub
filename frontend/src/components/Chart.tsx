import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import axios from 'axios';

// Define the StockData interface
interface StockData {
  date: string;
  close: number; // Only need the close price for the chart
}

// Define the Holdings interface
interface Holding {
  ticker: string;
  shares: number;
}

const Chart: React.FC = () => {
  const [chartData, setChartData] = useState<StockData[]>([]);
  const [holdings, setHoldings] = useState<Holding[]>([]);

  useEffect(() => {
    const fetchHoldings = async () => {
      try {
        const response = await axios.get('/api/portfolio/holdings'); // Fetch holdings
        const holdingsData = response.data.stocks; // Extract the stocks array
        setHoldings(holdingsData);

        // Now fetch historical prices for each holding
        const historicalPromises = holdingsData.map(async (holding: Holding) => {
          const pricesResponse = await axios.get(`https://financialmodelingprep.com/api/v3/historical-price-full/${holding.ticker}?apikey=YOUR_API_KEY`);
          return pricesResponse.data.historical.map((data: any) => ({
            date: data.date,
            close: data.close,
          }));
        });

        // Resolve all historical price promises
        const historicalDataArrays = await Promise.all(historicalPromises);
        
        // Flatten the array and merge with shares data (if needed)
        const combinedData = historicalDataArrays.flat();
        setChartData(combinedData);
        
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchHoldings();
  }, []);

  return (
    <div className="chart-container">
      <h1>Stock Price Chart</h1>
      <LineChart width={600} height={300} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="close" stroke="#8884d8" />
      </LineChart>
    </div>
  );
};

export default Chart;
