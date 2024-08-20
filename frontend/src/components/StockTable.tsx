import React from 'react';

const StockTable: React.FC<{ data: any[] }> = ({ data }) => {
  if (data.length === 0) {
    return <p>No data available</p>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Score</th>
          {/* Add other column headers as needed */}
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.symbol}</td>
            <td>{item.score}</td>
            {/* Add other columns as needed */}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StockTable;
