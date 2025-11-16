import React, { useState, useRef, useEffect } from 'react';
import Message from './Message';

const ChatInterface = ({ currentChat, onUpdateChat, onNewChat }) => {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages]);

  const handleSendMessage = () => {
    if (message.trim() && currentChat) {
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

      // Simulate AI response after 1 second
      setTimeout(() => {
        const aiMessage = {
          id: Date.now() + 1,
          text: getAIResponse(message.trim()),
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        };
        onUpdateChat(currentChat.id, [...updatedMessages, aiMessage]);
      }, 1000);
    }
  };

  const getAIResponse = (userMessage) => {
    const responses = [
      "I've analyzed your PDF and found some interesting insights. Based on the content, I can help explain the key concepts in more detail.",
      "That's a great question about the PDF! The document covers this topic extensively. Let me break it down for you.",
      "I understand you're looking for clarification. The PDF provides comprehensive information on this subject. Here's what I can tell you:",
      "Based on the PDF content, I can provide you with a detailed explanation. The document emphasizes several important points related to your question.",
      "I've reviewed the relevant sections of your PDF. Here's a comprehensive answer to your question:"
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handlePdfClick = (file) => {
    // Create a blob URL for the PDF file
    const fileUrl = URL.createObjectURL(file);
    // Open the PDF in a new tab
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
              <Message key={msg.id} message={msg} />
            )}
          </div>
        ))}
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
            />
            <button 
              className="send-btn" 
              onClick={handleSendMessage}
              disabled={!message.trim()}
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