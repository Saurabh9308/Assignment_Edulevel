import React, { useState } from 'react';
import HomeCenter from './components/HomeCenter';
import ChatInterface from './components/ChatInterface';
import './index.css';

const App = () => {
  const [currentChat, setCurrentChat] = useState(null);
  const [isChatStarted, setIsChatStarted] = useState(false);

  const handleFileUpload = (file) => {
    const newChat = {
      id: Date.now(),
      name: `PDF: ${file.name.substring(0, 20)}${file.name.length > 20 ? '...' : ''}`,
      fileName: file.name,
      file: file,
      messages: [
        {
          id: Date.now(),
          text: file.name,
          sender: 'user',
          timestamp: new Date(),
          type: 'pdf',
          file: file
        }
      ]
    };
    setCurrentChat(newChat);
    setIsChatStarted(true);
  };

  const handleNewChat = () => {
    setCurrentChat(null);
    setIsChatStarted(false);
  };

  const updateChatMessages = (chatId, newMessages) => {
    if (currentChat && currentChat.id === chatId) {
      setCurrentChat(prev => ({ ...prev, messages: newMessages }));
    }
  };

  return (
    <div className="app">
      {!isChatStarted ? (
        <HomeCenter onFileUpload={handleFileUpload} />
      ) : (
        <ChatInterface 
          currentChat={currentChat}
          onUpdateChat={updateChatMessages}
          onNewChat={handleNewChat}
        />
      )}
    </div>
  );
};

export default App;