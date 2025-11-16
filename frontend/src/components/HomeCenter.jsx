import React, { useState } from 'react';

const HomeCenter = ({ onFileUpload }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleFileUpload = (file) => {
    if (file && file.type === 'application/pdf') {
      onFileUpload(file);
    } else {
      alert('Please select a PDF file');
    }
  };

  const handleFileInput = (event) => {
    const file = event.target.files[0];
    handleFileUpload(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  return (
    <div className="home-center">
      <div className="welcome-section">
        <h1>Learn with PDF</h1>
        <p>Upload your PDF document and start learning with your AI Tutor</p>
        
        <div 
          className={`upload-area ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-content">
            <h3>Drop your PDF here or click to browse</h3>
            <p>Supports PDF files up to 10MB</p>
            
            <label htmlFor="pdf-upload" className="upload-btn">
              Choose PDF File
            </label>
            <input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileInput}
              style={{ display: 'none' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeCenter;