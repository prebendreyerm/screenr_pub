import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; // Ensure this file includes the dark mode styles
import DarkModeSwitch from './components/DarkModeSwitch';
import StocksTable from './components/StockTable';

const App: React.FC = () => {
  // Initialize state for dark mode
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);

  // Toggle dark mode state
  const toggleDarkMode = () => {
    setIsDarkMode(prevMode => !prevMode);
  };

  // Apply dark mode class based on state
  useEffect(() => {
    const body = document.body;
    if (isDarkMode) {
      body.classList.add('dark-mode');
    } else {
      body.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  const apiUrl = 'http://localhost:5000/api/stocks/scores';
  const columns = ['name', 'symbol', 'sector', 'score']


  return (
    <div className={`App ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <header className="App-header">
        <DarkModeSwitch isDarkMode={isDarkMode} toggleDarkMode={toggleDarkMode} />
        <h1>Screenr</h1>
        {/* Other components or content */}
      </header>
      <h1>Scores table</h1>
      <StocksTable apiUrl={apiUrl} columns={columns} />
    </div>
  );
};

export default App;
