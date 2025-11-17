import React, { useState, useRef, useEffect } from 'react';
import Message from './Message';
import ImageMessage from './ImageMessage';
import apiService from '../services/apiService';

const ChatInterface = ({ currentChat, onUpdateChat, onNewChat }) => {
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages]);

  const handleSendMessage = async () => {
    if (message.trim() && currentChat && !isLoading) {
      const userMessage = {
        id: Date.now(),
        text: message.trim(),
        sender: 'user',
        timestamp: new Date(),
        type: 'text'
      };

      const updatedMessages = [...(currentChat.messages || []), userMessage];
      onUpdateChat(currentChat.id, updatedMessages);
      setMessage('');
      setIsLoading(true);

      try {
        const response = await apiService.sendChatMessage(currentChat.topicId, message.trim());
        
        const aiMessage = {
          id: Date.now() + 1,
          text: response.answer,
          sender: 'ai',
          timestamp: new Date(),
          type: 'text',
          image: response.image_filename ? {
            id: response.image_id || `img_${Date.now()}`,
            filename: response.image_filename,
            title: response.image_title || 'Relevant Diagram',
            url: apiService.getImageUrl(response.image_filename)
          } : null
        };

        onUpdateChat(currentChat.id, [...updatedMessages, aiMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
        
        const errorMessage = {
          id: Date.now() + 1,
          text: "I'm having trouble connecting to the AI service. Please try again.",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        };
        
        onUpdateChat(currentChat.id, [...updatedMessages, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handlePdfClick = (file) => {
    const fileUrl = URL.createObjectURL(file);
    window.open(fileUrl, '_blank');
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-info">
          <div className="ai-tutor-logo">
            <div className="logo-icon">🧠</div>
            <span>AI-Tutor</span>
          </div>
          <div className="chat-subtitle">Tutor</div>
        </div>
        <div className="chat-actions">
          <button className="action-btn new-chat-btn" onClick={onNewChat}>
            <span>+ New Chat</span>
          </button>
        </div>
      </div>
      
      <div className="chat-messages">
        {currentChat?.messages?.map(msg => (
          <div key={msg.id}>
            {msg.type === 'pdf' ? (
              <div className="message user-message">
                <div className="message-avatar">👤</div>
                <div className="message-content-wrapper">
                  <div className="message-content">
                    <div 
                      className="pdf-message"
                      onClick={() => handlePdfClick(msg.file)}
                    >
                      <div className="pdf-icon">📄</div>
                      <div className="pdf-info">
                        <div className="pdf-name">{msg.text}</div>
                        <div className="pdf-type">PDF Document</div>
                      </div>
                      <div className="pdf-action">Click to view</div>
                    </div>
                    <div className="message-time">
                      {new Date(msg.timestamp).toLocaleTimeString('en-US', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <Message key={msg.id} message={msg} />
                {msg.sender === 'ai' && msg.image && (
                  <ImageMessage 
                    image={msg.image} 
                    timestamp={msg.timestamp}
                  />
                )}
              </>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-avatar">🤖</div>
            <div className="message-content-wrapper">
              <div className="message-content">
                <div className="message-text typing-indicator">
                  AI Tutor is thinking...
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="chat-input-container">
        <div className="input-wrapper">
          <div className="chat-input">
            <textarea
              placeholder="Message AI Tutor..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              rows="1"
              disabled={isLoading}
            />
            <button 
              className="send-btn" 
              onClick={handleSendMessage}
              disabled={!message.trim() || isLoading}
            >
              <span className="send-icon">➤</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;