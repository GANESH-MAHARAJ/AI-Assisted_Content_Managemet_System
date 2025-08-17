import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, Link } from 'react-router-dom';
import Landing from './pages/Landing';
import Admin from './pages/Admin';
import User from './pages/User';
import Login from './pages/Login';

// Updated dummy users with multiple users per role
const dummyUsers = {
  admin: [
    { username: 'admin', password: 'admin123' },
    { username: 'gan', password: 'gan' },
    { username: 'sspl', password: 'sspl' },
  ],
  user: [
    { username: 'user', password: 'user123' },
    { username: 'gan', password: 'gan' },
    { username: 'sspl', password: 'sspl' },
  ],
};

// Styles for buttons and header
const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center',
    padding: '20px',
    marginTop: '20px',
    color: '#333',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
    padding: '10px',
    backgroundColor: '#f4f4f4',
    borderRadius: '8px',
  },
  homeButton: {
    padding: '8px 16px',
    backgroundColor: '#003366',
    color: '#ffffff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    textDecoration: 'none',
  },
  username: {
    fontSize: '1.1rem',
    fontWeight: '600',
    color: '#555',
  },
  welcomePart: {
    marginBottom: '20px',
    fontSize: '1.4rem',
    fontWeight: '600',
    color: '#555',
  },
};

function AppContent({ loggedIn, userRole, username, handleLogin, handleLogout }) {
  const location = useLocation();

  // Check if the current page is Admin or User page
  const isUserOrAdminPage = location.pathname === '/admin' || location.pathname === '/user';

  return (
    <div style={styles.container}>
      {/* Header with Home button on left and username on right, only on Admin/User pages */}
      {location.pathname !== '/' && (
        <div style={styles.header}>
          <Link to="/" style={styles.homeButton}>Home</Link>
          {/* Show username only on Admin or User pages */}
          {loggedIn && isUserOrAdminPage && (
            <div style={styles.username}>
              {`User: ${username}`}
            </div>
          )}
        </div>
      )}

      {/* Welcome message only on Admin or User pages */}
      {loggedIn && isUserOrAdminPage && (
        <div style={styles.welcomePart}>
          {`Welcome, ${userRole.toUpperCase()}!`}
        </div>
      )}

      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route
          path="/admin"
          element={
            loggedIn && userRole === 'admin' ? (
              <Admin onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
        <Route
          path="/user"
          element={
            loggedIn && userRole === 'user' ? (
              <User onLogout={handleLogout} />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />
      </Routes>
    </div>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userRole, setUserRole] = useState(null);
  const [username, setUsername] = useState('');

const handleLogin = (inputUsername, inputPassword, role) => {
  if (role === 'admin') {
    // Check only admin users
    const adminUser = dummyUsers.admin.find(
      (user) => user.username === inputUsername && user.password === inputPassword
    );
    if (adminUser) {
      setLoggedIn(true);
      setUserRole('admin');
      setUsername(adminUser.username);
      return 'admin';
    }
  } else if (role === 'user') {
    // Check only user users
    const normalUser = dummyUsers.user.find(
      (user) => user.username === inputUsername && user.password === inputPassword
    );
    if (normalUser) {
      setLoggedIn(true);
      setUserRole('user');
      setUsername(normalUser.username);
      return 'user';
    }
  }

  alert('Invalid username or password');
  return null;
};





  const handleLogout = () => {
    setLoggedIn(false);
    setUserRole(null);
    setUsername('');
  };

  return (
    <Router>
      <AppContent
        loggedIn={loggedIn}
        userRole={userRole}
        username={username}
        handleLogin={handleLogin}
        handleLogout={handleLogout}
      />
    </Router>
  );
}

export default App;
