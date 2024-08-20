import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import StockTable from './components/StockTable'; // Import your StockTable component
import './App.css'; // Import your custom CSS
import DarkModeSwitch from './components/DarkModeSwitch';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);
  const [data, setData] = useState<any[]>([]); // Add state for storing stock data
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('bg-dark', 'text-light');
    } else{
      document.body.classList.remove('bg-dark', 'text-light');
    }
  }, [isDarkMode]);

  useEffect(() => {
    // Fetch stock data from the API
    fetch(`http://127.0.0.1:5000/api/stocks/scores?page=${page}&per_page=100`) // Update the URL to include the page and per_page parameters
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        setData(prevData => [...prevData, ...data]);
        if (data.length < 100) {
          setHasMore(false); // No more data to load
        }
      })
      .catch((error) => console.error('Error fetching data:', error));
  }, [page]);

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  const loadMore = () => {
    if (hasMore) {
      setPage(prevPage => prevPage + 1);
    }
  };

  return (
    <div className={`container-fluid ${isDarkMode ? 'bg-dark text-light' : 'bg-light text-dark'}`}>
      <div className="d-flex justify-content-between align-items-center py-3">
        <h1>Stock Data</h1>
        <DarkModeSwitch isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
      </div>
      <div className="my-4">
        <StockTable data={data} />
        {hasMore && (
          <button className="btn btn-primary mt-3" onClick={loadMore}>
            Load More
          </button>
        )}
      </div>
    </div>
  );
};

export default App;
