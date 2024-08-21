import React from "react";

interface StrategyDropdownProps {
  strategy: string;
  onStrategyChange: (newStrategy: string) => void;
}

const StrategyDropdown: React.FC<StrategyDropdownProps> = ({ strategy, onStrategyChange }) => {
  return (
    <div className="form-group">
      <label htmlFor="strategySelect">Select Strategy:</label>
      <select
        id="strategySelect"
        className="form-control"
        value={strategy}
        onChange={(e) => onStrategyChange(e.target.value)}
      >
        <option value="baseline">Baseline</option>
        <option value="baseline_Technology">Technology</option>
        <option value="baseline_Basic Materials">Basic Materials</option>
        <option value="baseline_Communication Services">Communication Services</option>
        <option value="baseline_Consumer Cyclical">Consumer Cyclical</option>
        <option value="baseline_Consumer Goods">Consumer Goods</option>
        <option value="baseline_Consumer Services">Consumer Services</option>
        <option value="baseline_Consumer Staples">Consumer Staples</option>
        <option value="baseline_Energy">Energy</option>
        <option value="baseline_Finance">Finance</option>
        <option value="baseline_Financials">Financials</option>
        <option value="baseline_Health Care">Health Care</option>
        <option value="baseline_Industrials">Industrials</option>
        <option value="baseline_Miscellaneous">Miscellaneous</option>
        <option value="baseline_Real Estate">Real Estate</option>
        <option value="baseline_Telecommunications">Telecommunications</option>
        <option value="baseline_Utilities">Utilities</option>
        {/* Add more strategies as needed */}
      </select>
    </div>
  );
};

export default StrategyDropdown;
