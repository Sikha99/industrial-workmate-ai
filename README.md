# Industrial WorkMate AI

A local AI assistant that helps users understand factory work management procedures and perform basic shift management operations using AI.

## Overview

Industrial WorkMate AI uses Retrieval-Augmented Generation (RAG) to answer factory-related questions using information from a custom knowledge base.

The application also supports basic shift management through natural-language requests. Users can create and view shifts by interacting with the assistant. Shift information is stored in a SQLite database.

The project is developed using open-source technologies to understand and implement practical AI applications.

## Technology Stack

- **Language:** Python
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **LLM Runtime:** Ollama
- **Language Model:** Qwen 2.5 1.5B
- **Workflow:** LangGraph
- **Backend:** FastAPI
- **Database:** SQLite
- **User Interface:** Streamlit

LangGraph is used to manage different workflows in the application. As the project grows to include training management, worker skills, and shift assignments, it will help manage these connected workflows.

## Current Features

- Custom factory knowledge base
- Text chunking and embedding generation
- Semantic search using ChromaDB
- Local LLM integration through Ollama
- Context-based answers using RAG
- Fallback responses for unsupported questions
- Interactive chat interface using Streamlit
- Natural-language shift creation
- View existing shifts through chat
- Extract and validate shift details using an LLM
- Ask follow-up questions when shift details are missing
- Store shift information in SQLite
- FastAPI integration for handling chat requests
- LangGraph workflow to manage different user requests

## Architecture

1. Load the factory knowledge source.
2. Split documents into smaller text chunks.
3. Generate embeddings using Sentence Transformers.
4. Store the text and embeddings in ChromaDB.
5. Receive user questions through the chat interface.
6. Identify the user's intent using an LLM.
7. Use LangGraph to route the request.
8. For factory questions, retrieve relevant information from ChromaDB and generate an answer using the local LLM.
9. For shift requests, extract and validate the required details.
10. Ask follow-up questions if any required details are missing.
11. Store shift information in SQLite and return the response.

> This project is being developed step by step to learn and implement RAG, LangGraph, FastAPI, and database integration using open-source technologies.
