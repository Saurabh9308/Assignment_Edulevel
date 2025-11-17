# RAG Tutor Frontend

Lightweight React + Vite client for the AI tutor. The UI stays minimal on purpose:

- Landing screen with a single drop zone / picker for PDFs (drag-and-drop supported).
- Chat screen that looks like a messenger thread: user and AI bubbles, plus inline diagrams only when the backend returns one for that answer.
- No extra cards, galleries, or banners—just upload, ask, and read the response.

## Run Locally
```bash
cd /Users/sk__volley__07/Desktop/New\ Beginning/Assignment_Edulevel/frontend
npm install
npm run dev -- --host
```

Open the Vite URL shown in the terminal (usually `http://127.0.0.1:5173`). Make sure the FastAPI backend is already running at `http://localhost:8000`.

## Environment Variables (optional)
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_ASSET_BASE_URL=http://localhost:8000
```

## Source Overview
```
src/
  components/
    ChatInterface.jsx   # Chat layout + message list
    HomeCenter.jsx      # Upload landing screen
    ImageMessage.jsx    # Inline diagram bubble
    Message.jsx         # Generic text bubble
  services/
    apiService.js       # Fetch helpers + image URL builder
  App.jsx               # High-level state + routing between views
  index.css             # Simple dark theme styling
```

All styling lives in `index.css`. Tweak the CSS variables at the top if you want a different color palette, but the layout intentionally stays straightforward so learners focus on the conversation.
