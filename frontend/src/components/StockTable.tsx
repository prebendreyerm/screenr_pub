import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface StocksTableProps {
  apiUrl: string;
  columns: string[];
}

const StocksTable: React.FC<StocksTableProps> = ({ apiUrl, columns }) => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(apiUrl);
        setData(response.data.data);
        setLoading(false);
      } catch (err) {
        setLoading(false);
        setError('An error occurred while fetching data.');
      }
    };

    fetchData();
  }, [apiUrl]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              {columns.map(column => (
                <td key={column}>{item[column]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StocksTable;
