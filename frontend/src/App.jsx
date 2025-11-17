import React, { useState } from 'react';
import HomeCenter from './components/HomeCenter';
import ChatInterface from './components/ChatInterface';
import apiService from './services/apiService';
import './index.css';

const App = () => {
  const [currentChat, setCurrentChat] = useState(null);
  const [isChatStarted, setIsChatStarted] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (file) => {
    if (!file) return;

    setIsUploading(true);
    
    try {
      const uploadResponse = await apiService.uploadPDF(file);
      
      const newChat = {
        id: Date.now(),
        topicId: uploadResponse.topic_id,
        name: `PDF: ${file.name.substring(0, 20)}${file.name.length > 20 ? '...' : ''}`,
        fileName: file.name,
        file,
        messages: [
          {
            id: Date.now(),
            text: `PDF uploaded: ${file.name}`,
            sender: 'system',
            timestamp: new Date(),
            type: 'pdf',
            file
          },
          {
            id: Date.now() + 1,
            text: `I've processed your PDF (${uploadResponse.chunks_processed} sections). Ask me anything about the content!`,
            sender: 'ai',
            timestamp: new Date(),
            type: 'text'
          }
        ]
      };
      
      setCurrentChat(newChat);
      setIsChatStarted(true);
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Failed to upload PDF. Please try again.');
    } finally {
      setIsUploading(false);
    }
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
        <HomeCenter onFileUpload={handleFileUpload} isUploading={isUploading} />
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