import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

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
  const itemsPerPage = 20;

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
  }, [apiUrl, columns, currentPage, sortBy, sortOrder, searchQuery]); // Include searchQuery as a dependency

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

  const handleSearchKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      setSearchQuery(inputQuery); // Update searchQuery to trigger useEffect
    }
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
      <table className="table table-dark">
        <thead>
          <tr>
            {columns.map(column => (
              <th key={column.key} onClick={() => handleSort(column.key)}>
                {column.label} {sortBy === column.key ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
              </th>
            ))}
          </tr>
          <tr>
            {columns.map(column => (
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
              {columns.map(column => (
                <td key={column.key}>{item[column.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className='pagination'>
        <button type="button" className='btn btn-primary' onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
          Previous
        </button>
        <span> Page {currentPage} of {totalPages} </span>
        <button type="button" className='btn btn-primary' onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default StocksTable;
