import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const styles = {
  container: {
    maxWidth: 400,
    margin: '50px auto',
    padding: 20,
    borderRadius: 8,
    boxShadow: '0 2px 12px rgba(0,0,0,0.12)',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    backgroundColor: '#fff',
    textAlign: 'center',
  },
  input: {
    width: '80%',
    padding: '10px',
    margin: '8px 0',
    borderRadius: 5,
    border: '1px solid #bbb',
    fontSize: '1rem',
  },
  button: {
    padding: '10px 20px',
    fontSize: '1rem',
    borderRadius: 5,
    border: 'none',
    backgroundColor: '#28a745',
    color: 'white',
    cursor: 'pointer',
  },
  error: {
    color: 'red',
    marginTop: 8,
  },
};

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  // Extract role from the URL query parameter
  const params = new URLSearchParams(location.search);
  const role = params.get('role'); // 'admin' or 'user'

  const handleSubmit = (e) => {
    e.preventDefault();
    const userRole = onLogin(username, password, role);
    if (userRole) {
      navigate(`/${userRole}`);
    } else {
      setError('Invalid credentials. Please try again.');
    }
  };

  return (
    <div style={styles.container}>
      <h2>{role === 'admin' ? 'Admin' : 'User'} Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>
          Login
        </button>
        {error && <div style={styles.error}>{error}</div>}
      </form>
    </div>
  );
}
