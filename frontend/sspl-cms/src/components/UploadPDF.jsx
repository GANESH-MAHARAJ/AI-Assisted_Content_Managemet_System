import React, { useState } from 'react';

const styles = {
  input: {
    padding: '10px',
    fontSize: '1rem',
    borderRadius: 4,
    border: '1px solid #ccc',
  },
  button: {
    marginLeft: 10,
    padding: '10px 18px',
    fontSize: '1rem',
    borderRadius: 4,
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
  },
  buttonDisabled: {
    backgroundColor: '#6c757d',
    cursor: 'not-allowed',
  },
};

export default function UploadPDF() {
  const [pdfFile, setPdfFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) {
      alert('Please select a PDF file first.');
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('pdf', pdfFile);

    try {
      const response = await fetch('http://localhost:5000/upload_pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert('Upload failed: ' + (errorData.error || response.statusText));
        setUploading(false);
        return;
      }

      const data = await response.json();
      alert(data.message);
      setPdfFile(null);
    } catch (error) {
      alert('Error uploading file: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        style={styles.input}
        disabled={uploading}
      />
      <button
        onClick={handleUpload}
        style={{ 
          ...styles.button, 
          ...(uploading ? styles.buttonDisabled : {}) 
        }}
        disabled={uploading}
      >
        {uploading ? 'Uploading...' : 'Upload PDF'}
      </button>
    </div>
  );
}
