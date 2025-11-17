import React, { useRef, useState } from 'react';

const HomeCenter = ({ onFileUpload, isUploading }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const isPdfFile = (file) => {
    if (!file) return false;
    if (file.type === 'application/pdf') return true;
    return (file.name || '').toLowerCase().endsWith('.pdf');
  };

  const handleFileUpload = (file) => {
    if (file && isPdfFile(file)) {
      onFileUpload(file);
    } else if (file) {
      alert('Please select a PDF file (.pdf extension)');
    }
  };

  const handleFileInput = (event) => {
    const file = event.target.files[0];
    handleFileUpload(file);
    event.target.value = '';
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
          className={`upload-area ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="upload-content">
            {isUploading ? (
              <>
                <h3>Processing PDF...</h3>
                <p>This may take a few moments</p>
                <div className="loading-spinner"></div>
              </>
            ) : (
              <>
                <h3>Drop your PDF here or click to browse</h3>
                <p>Supports PDF files up to 10MB</p>
                
                <label 
                  htmlFor="pdf-upload" 
                  className="upload-btn"
                  onClick={() => fileInputRef.current?.click()}
                >
                  Choose PDF File
                </label>
                <input
                  id="pdf-upload"
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInput}
                  style={{ display: 'none' }}
                  ref={fileInputRef}
                />
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeCenter;