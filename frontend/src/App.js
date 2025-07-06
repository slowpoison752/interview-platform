import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a PDF file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Use environment variable for API URL in production
      const apiUrl = process.env.REACT_APP_API_URL || '/api';
      const response = await axios.post(`${apiUrl}/upload-resume`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing the file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>📄 Resume Parser</h1>
          <p>Upload your resume and get instant insights</p>
        </header>

        <main className="main">
          <div className="upload-section">
            <form onSubmit={handleSubmit} className="upload-form">
              <div className="file-input-container">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  id="file-input"
                  className="file-input"
                />
                <label htmlFor="file-input" className="file-input-label">
                  {file ? file.name : 'Choose PDF file'}
                </label>
              </div>

              <button
                type="submit"
                disabled={!file || loading}
                className="submit-button"
              >
                {loading ? 'Processing...' : 'Parse Resume'}
              </button>
            </form>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
          </div>

          {result && (
            <div className="result-section">
              <h2>📋 Resume Analysis</h2>
              
              <div className="result-grid">
                <div className="result-card">
                  <h3>📧 Contact Information</h3>
                  {result.sections.contact_info.email && (
                    <p><strong>Email:</strong> {result.sections.contact_info.email}</p>
                  )}
                  {result.sections.contact_info.phone && (
                    <p><strong>Phone:</strong> {result.sections.contact_info.phone}</p>
                  )}
                </div>

                <div className="result-card">
                  <h3>🛠️ Key Skills</h3>
                  <div className="skills-list">
                    {result.sections.skills.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))}
                  </div>
                </div>

                <div className="result-card full-width">
                  <h3>📝 Summary</h3>
                  <p>{result.sections.summary || 'No summary available'}</p>
                </div>

                <div className="result-card full-width">
                  <h3>📄 Raw Text (First 500 chars)</h3>
                  <div className="raw-text">
                    <pre>{result.raw_text}</pre>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App; 