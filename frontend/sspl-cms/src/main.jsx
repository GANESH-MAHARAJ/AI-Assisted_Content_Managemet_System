import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import styles from './Main.module.css';
import logo from './assets/logo.png';
// import buildingPic from './assets/building.png';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <div className={styles.mainContainer}>
      <header className={styles.header}>
        <img src={logo} alt="Logo" className={styles.logo} />
        <h1>SSPL Content Management System</h1>
      </header>
      
      <App />
    </div>
  </StrictMode>
);
