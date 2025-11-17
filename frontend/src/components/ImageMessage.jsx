import React, { useState } from 'react';

const ImageMessage = ({ image, timestamp }) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoading(false);
  };

  const handleImageLoad = () => {
    setImageLoading(false);
  };

  if (!image || !image.url) return null;

  return (
    <div className="message ai-message">
      <div className="message-avatar">🤖</div>
      <div className="message-content-wrapper">
        <div className="message-content">
          <div className="image-message">
            {imageLoading && (
              <div className="image-loading">
                <div className="loading-spinner small"></div>
                <span>Loading image...</span>
              </div>
            )}
            {!imageError ? (
              <img 
                src={image.url} 
                alt={image.title}
                className="message-image"
                onError={handleImageError}
                onLoad={handleImageLoad}
                style={{ display: imageLoading ? 'none' : 'block' }}
              />
            ) : (
              <div className="image-error">
                <div className="error-icon">⚠️</div>
                <span>Failed to load image</span>
              </div>
            )}
            <div className="image-caption">{image.title}</div>
          </div>
          <div className="message-time">
            {formatTime(timestamp)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImageMessage;