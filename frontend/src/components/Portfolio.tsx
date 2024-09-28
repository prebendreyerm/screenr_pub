import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

const Portfolio: React.FC = () => {
  return (
    <div className="container">
      <div className="row justify-content-left">
        
        {/* Cash Input Field - Smaller Width */}
        <div className="col-12 col-md-4 mb-3"> {/* Adjust width as needed */}
          <div className="input-group">
            <span className="input-group-text bg-dark text-light" id="basic-addon1">Cash</span>
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Amount" 
              aria-label="Cash" 
              aria-describedby="basic-addon1"
            />
            <button
              className="btn btn-outline-light rounded-start" // Square edges on the left
              type="button"
              id="button-addon1">Deposit</button>
            <button
              className="btn btn-outline-light rounded-end" // Square edges on the right
              type="button"
              id="button-addon2">Withdraw</button>
          </div>
        </div>

      </div>

      {/* New Row for Stock Input Fields */}
      <div className="row justify-content-left">
        <div className="col-12 col-md-7 mb-3"> {/* Adjust width as needed */}
          <div className="input-group mb-2">
            <span className="input-group-text bg-dark text-light" id="basic-addon3">Stock</span>
            <input 
              type="text" 
              className="form-control bg-dark text-light" 
              placeholder="Ticker" 
              aria-label="Ticker" 
              aria-describedby="basic-addon3"
            />
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Shares" 
              aria-label="Shares" 
              aria-describedby="basic-addon4"
            />
            <input 
              type="number" 
              className="form-control bg-dark text-light" 
              placeholder="Cost" 
              aria-label="Cost" 
              aria-describedby="basic-addon5"
            />
            <input 
              type="date" 
              className="form-control bg-dark text-light" 
              aria-label="Date" 
              aria-describedby="basic-addon6"
            />
            {/* Add buttons without input-group, remove margin */}
            <button
              className="btn btn-outline-light rounded-start" // Rounded edges for Buy button
              type="button"
              id="button-addon7">Buy</button>
            <button
              className="btn btn-outline-light rounded-end" // Rounded edges for Sell button
              type="button"
              id="button-addon8">Sell</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
