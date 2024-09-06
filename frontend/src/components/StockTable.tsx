import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

interface StocksTableProps {
  apiUrl: string;
  columns: { key: string, label: string }[];
}

interface Stock {
  [key: string]: any;
}

const StocksTable: React.FC<StocksTableProps> = ({ apiUrl, columns }) => {
  const [data, setData] = useState<Stock[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalItems, setTotalItems] = useState<number>(0);
  const [sortBy, setSortBy] = useState<string>(''); 
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [searchQuery, setSearchQuery] = useState<{ name: string, symbol: string, sector: string }>({
    name: '',
    symbol: '',
    sector: ''
  });
  const [inputQueries, setInputQueries] = useState<{ name: string, symbol: string, sector: string }>({
    name: '',
    symbol: '',
    sector: ''
  });
  const [strategyQuery, setStrategyQuery] = useState<string>('baseline');

  const itemsPerPage = 19;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(apiUrl, {
          params: {
            columns: columns.map(col => col.key).join(','), 
            page: currentPage,
            limit: itemsPerPage,
            sort_by: sortBy || undefined,
            sort_order: sortOrder,
            name_search: searchQuery.name || undefined,
            symbol_search: searchQuery.symbol || undefined,
            sector_search: searchQuery.sector || undefined,
            strategy: strategyQuery || undefined,
          },
        });
        setData(response.data.data);
        setTotalItems(response.data.total);
        setLoading(false);
      } catch (err) {
        setLoading(false);
        setError('An error occurred while fetching data.');
      }
    };

    fetchData();
  }, [apiUrl, columns, currentPage, sortBy, sortOrder, searchQuery, strategyQuery]); // Include searchQuery as a dependency

  const handleSort = (column: string) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
    setCurrentPage(1);
  };

  const handleSearchChange = (key: 'name' | 'symbol' | 'sector') => (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputQueries({ ...inputQueries, [key]: e.target.value });
  };

  const handleSearchKeyDown = (key: 'name' | 'symbol' | 'sector') => (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      setSearchQuery({ ...searchQuery, [key]: inputQueries[key] }); // Update searchQuery to trigger useEffect
    }
  };

  const handleStrategyChange = (strategy: string) => {
    setStrategyQuery(strategy);
    setCurrentPage(1); // Reset to first page when strategy changes
  };
  

  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= Math.ceil(totalItems / itemsPerPage)) {
      setCurrentPage(newPage);
    }
  };

  if (loading) return (
    <div class="spinner-border" role="status">
    </div>
  )
  if (error) return <p>Error: {error}</p>;

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  return (
    <div className="table-container">
      <div className="dropdown mb-3">
        <button
          className="btn btn-primary btn-sm dropdown-toggle"
          type="button"
          id="dropdownMenuButton"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Strategy
        </button>
        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline')}>Baseline</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_technology')}>Technology</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Basic Materials')}>Basic Materials</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Communication Services')}>Communication Services</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Consumer Cyclical')}>Consumer Cyclical</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Consumer Goods')}>Consumer Goods</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Consumer Staples')}>Consumer Staples</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Energy')}>Energy</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Financials')}>Financials</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Telecommunications')}>Telecommunications</button>
          </li>
          <li>
            <button className="dropdown-item" onClick={() => handleStrategyChange('baseline_Utilities')}>Utilities</button>
          </li>
          {/* Add more strategies as needed */}
        </ul>
      </div>

      <table className="table table-dark">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} onClick={() => handleSort(column.key)}>
                {column.label} {sortBy === column.key ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
              </th>
            ))}
          </tr>
          <tr>
            {columns.map((column) => (
              <td key={column.key} className={`search-cell ${column.key === 'name' ? 'active' : ''}`}>
                {column.key === 'name' && (
                  <input
                    type="text"
                    placeholder="Search by name"
                    value={inputQueries.name}
                    onChange={handleSearchChange('name')}
                    onKeyDown={handleSearchKeyDown('name')}
                    className="search-input"
                  />
                )}
                {column.key === 'symbol' && (
                  <input
                    type="text"
                    placeholder="Search by ticker"
                    value={inputQueries.symbol}
                    onChange={handleSearchChange('symbol')}
                    onKeyDown={handleSearchKeyDown('symbol')}
                    className="search-input"
                  />
                )}
                {column.key === 'sector' && (
                  <input
                    type="text"
                    placeholder="Search by sector"
                    value={inputQueries.sector}
                    onChange={handleSearchChange('sector')}
                    onKeyDown={handleSearchKeyDown('sector')}
                    className="search-input"
                  />
                )}
              </td>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.key}>{item[column.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
  
      <div className="pagination">
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span> Page {currentPage} of {totalPages} </span>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default StocksTable;