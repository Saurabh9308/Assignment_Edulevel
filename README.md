# RAG-Based AI Tutor with Inline Images

## Project Overview

This project demonstrates a small, fully local Retrieval-Augmented Generation (RAG) tutor capable of ingesting a chapter PDF, answering follow-up questions, and dynamically surfacing the most relevant diagram in-line with every answer. It's designed to provide a rich, contextually aware learning experience by combining textual answers with visual aids directly extracted from the study material.

The tutor operates without requiring external LLM API keys, leveraging local TF-IDF embeddings and FAISS for efficient information retrieval and a lightweight, grounded answering mechanism.

## Architecture Overview

The system is composed of a FastAPI backend service and a Vite + React frontend single-page application, along with a static file server for serving diagrams.

http://googleusercontent.com/image_generation_content/1



**Key Components:**

* **Frontend (Vite + React SPA):** Handles user interaction, PDF uploads, displays chat conversations, and renders inline images.
* **Backend (FastAPI Service):** The core logic, including PDF ingestion, text chunking, TF-IDF embedding generation, FAISS vector storage, retrieval for both text and images, and grounded answer generation.
* **Static File Server (`backend/data/`):** Serves persisted PDFs, FAISS indices, metadata JSON, and the actual diagram assets referenced by the chat responses.

## Features

* **PDF Ingestion:** Upload any PDF chapter for study.
* **Contextual Q&A:** Ask questions about the uploaded material and receive grounded answers.
* **Inline Diagram Retrieval:** Automatically surfaces the most relevant diagram with each answer, enhancing comprehension.
* **Fully Local:** Runs entirely on your machine without needing external API calls for LLMs.
* **Persistent Data:** Uploaded PDFs, embeddings, and associated metadata are persisted for continued use.

## Project Layout
