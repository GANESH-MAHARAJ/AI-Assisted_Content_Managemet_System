import React, { useState } from 'react';

const styles = {
  container: {
    maxWidth: 600,
    margin: '40px auto',
    padding: 20,
    borderRadius: 8,
    boxShadow: '0 2px 12px rgba(0,0,0,0.12)',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    backgroundColor: '#fff',
    textAlign: 'center',
  },
  heading: {
    marginBottom: 25,
    color: '#222',
  },
  input: {
    width: '70%',
    padding: '12px',
    fontSize: '1.1rem',
    borderRadius: 5,
    border: '1px solid #bbb',
  },
  button: {
    marginLeft: 12,
    padding: '12px 22px',
    fontSize: '1.1rem',
    borderRadius: 5,
    border: 'none',
    backgroundColor: '#28a745',
    color: 'white',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
  },
  buttonLogout: {
    marginTop: 30,
    padding: '10px 24px',
    fontSize: '1rem',
    borderRadius: 5,
    border: 'none',
    backgroundColor: '#dc3545',
    color: 'white',
    cursor: 'pointer',
  },
  resultsList: {
    marginTop: 30,
    listStyleType: 'none',
    padding: 0,
    maxHeight: 300,
    overflowY: 'auto',
    textAlign: 'left',
  },
  resultItem: {
    marginBottom: 10,
    padding: 10,
    borderRadius: 5,
    border: '1px solid #ddd',
    backgroundColor: '#fafafa',
  },
  resultLink: {
    color: '#007bff',
    textDecoration: 'none',
    fontWeight: '600',
  },
  tags: {
    fontSize: '0.85rem',
    color: '#555',
    marginTop: 4,
  }
};

export default function User({ onLogout }) {
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keywords.trim()) {
      alert('Please enter keywords to search.');
      return;
    }
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/search_pdfs?keywords=${encodeURIComponent(keywords)}`);
      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      alert(`Search failed: ${error.message}`);
      setResults([]);
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>User Dashboard</h2>

      <input
        type="text"
        placeholder="Enter keywords"
        value={keywords}
        onChange={(e) => setKeywords(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter') handleSearch(); }}
        style={styles.input}
        disabled={loading}
      />
      <button onClick={handleSearch} style={styles.button} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>

      <ul style={styles.resultsList}>
        {results.length === 0 && !loading && <li>No results found.</li>}
        {results.map((doc, idx) => (
          <li key={idx} style={styles.resultItem}>
            <a
              href={`http://localhost:5000/get_pdf/${encodeURIComponent(doc.file_name)}`}
              target="_blank"
              rel="noreferrer"
              style={styles.resultLink}
            >
              {doc.file_name}
            </a>
            <div style={styles.tags}>Tags: {doc.tags?.join(', ')}</div>
          </li>
        ))}
      </ul>

      <button onClick={onLogout} style={styles.buttonLogout}>Logout</button>
    </div>
  );
}
