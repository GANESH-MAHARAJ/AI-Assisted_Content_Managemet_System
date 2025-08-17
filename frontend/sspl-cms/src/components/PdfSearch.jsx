import React, { useState } from 'react';

function PdfSearch() {
  const [keywords, setKeywords] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!keywords.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:5000/search_pdfs?keywords=${encodeURIComponent(keywords)}`);
      const data = await res.json();
      setResults(data.results || []);
    } catch (error) {
      alert('Error fetching search results');
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Search PDFs</h2>
      <input
        type="text"
        placeholder="Enter keywords"
        value={keywords}
        onChange={(e) => setKeywords(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
      />
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      <ul>
        {results.map(({ file_name, tags }) => (
          <li key={file_name}>
            <a href={`http://localhost:5000/get_pdf/${encodeURIComponent(file_name)}`} target="_blank" rel="noopener noreferrer">
              {file_name}
            </a>
            <br />
            <small>Tags: {tags.join(', ')}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PdfSearch;
