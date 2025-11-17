const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const defaultHeaders = {
  'Accept': 'application/json'
};

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      ...defaultHeaders,
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || response.statusText);
  }

  return response.json();
}

class ApiService {
  async uploadPDF(file) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      return await request('/upload', {
        method: 'POST',
        body: formData,
        headers: {} // browser sets multipart boundaries automatically
      });
    } catch (error) {
      console.error('PDF upload error:', error);
      throw error;
    }
  }

  async sendChatMessage(topicId, question) {
    try {
      return await request('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic_id: topicId,
          question: question,
        }),
      });
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }

  async getTopicImages(topicId) {
    try {
      return await request(`/images/${topicId}`, { method: 'GET' });
    } catch (error) {
      console.error('Images fetch error:', error);
      throw error;
    }
  }

  // Updated: Proper image URL construction
  getImageUrl(filename) {
    if (!filename) return null;
    const base = (import.meta.env.VITE_ASSET_BASE_URL || 'http://localhost:8000');
    return `${base}/static/images/${filename}`;
  }
}

export default new ApiService();