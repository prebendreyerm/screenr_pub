import React from "react";

interface DarkModeSwitchProps {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const DarkModeSwitch: React.FC<DarkModeSwitchProps> = ({ isDarkMode, toggleDarkMode }) => {
  return (
    <div className="form-check form-switch">
      <input
        className="form-check-input"
        type="checkbox"
        id="darkModeSwitch"
        checked={isDarkMode}
        onChange={toggleDarkMode}
      />
      <label className="form-check-label" htmlFor="darkModeSwitch">
        Dark Mode
      </label>
    </div>
  );
};

export default DarkModeSwitch;
