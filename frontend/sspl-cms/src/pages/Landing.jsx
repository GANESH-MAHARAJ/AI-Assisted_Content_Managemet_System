import React from 'react';
import { useNavigate } from 'react-router-dom';

const styles = {

  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    // justifyContent: 'center',
    // minHeight: '100vh',
    backgroundColor: '#f3f4f6',  // light gray background
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  
  heading: {
    fontSize: '2.5rem',
    fontWeight: '800',
    color: '#1f2937',  // dark gray
    marginBottom: '20px',
  },
  subheading: {
    fontSize: '1.2rem',
    color: '#4b5563',  // medium gray
    marginBottom: '40px',
  },
  buttonGroup: {
    display: 'flex',
    gap: '20px',
  },
  button: {
    padding: '12px 30px',
    fontSize: '1.1rem',
    fontWeight: '600',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    cursor: 'pointer',
    border: 'none',
    transition: 'transform 0.3s ease, background-color 0.3s ease',
    userSelect: 'none',
  },
  adminButton: {
    backgroundColor: '#3b82f6',  // blue
    color: 'white',
  },
  userButton: {
    backgroundColor: '#22c55e',  // green
    color: 'white',
  },
};

const Landing = () => {
  const navigate = useNavigate();

  const handleMouseEnter = (e) => {
    e.currentTarget.style.transform = 'scale(1.05)';
  };

  const handleMouseLeave = (e) => {
    e.currentTarget.style.transform = 'scale(1)';
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Welcome to SSPL CMS</h1>
      <p style={styles.subheading}>Manage and search your PDF files efficiently.</p>
      <div style={styles.buttonGroup}>
        <button
  style={{ ...styles.button, ...styles.adminButton }}
  onClick={() => navigate('/login?role=admin')}
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseLeave}
>
  Login as Admin
</button>
<button
  style={{ ...styles.button, ...styles.userButton }}
  onClick={() => navigate('/login?role=user')}
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseLeave}
>
  Login as User
</button>

      </div>
    </div>
  );
};

export default Landing;
