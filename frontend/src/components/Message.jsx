import React from 'react';

const Message = ({ message }) => {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className={`message ${message.sender}-message`}>
      <div className="message-avatar">
        {message.sender === 'ai' ? '🤖' : '👤'}
      </div>
      <div className="message-content-wrapper">
        <div className="message-content">
          <div className="message-text">
            {message.text}
          </div>
          <div className="message-time">
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Message;