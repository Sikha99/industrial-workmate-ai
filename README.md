\# Industrial WorkMate AI



A local AI assistant that helps users understand factory work management procedures using Retrieval-Augmented Generation (RAG).



\## Overview



Industrial WorkMate AI combines semantic search with a locally running Large Language Model (LLM) to retrieve relevant information from a custom factory knowledge base and generate context-aware answers.



The project demonstrates an end-to-end RAG pipeline using open-source technologies, with a focus on reliable information retrieval and practical factory work management assistance.



\## Technology Stack



\- \*\*Language:\*\* Python

\- \*\*Embeddings:\*\* Sentence Transformers

\- \*\*Vector Database:\*\* ChromaDB

\- \*\*LLM Runtime:\*\* Ollama

\- \*\*Language Model:\*\* Qwen 2.5 1.5B

\- \*\*User Interface:\*\* Streamlit



\## Current Features



\- Custom factory knowledge base

\- Text chunking and embedding generation

\- Semantic search and relevant context retrieval

\- Vector storage and similarity search using ChromaDB

\- Local LLM integration through Ollama

\- Similarity-threshold-based retrieval filtering

\- Context-grounded answer generation using RAG

\- Fallback responses for unsupported questions

\- Interactive chat interface using Streamlit

\- Evaluation dataset and results for testing question-answering behavior



\## Architecture



1\. Load the factory knowledge source.

2\. Split documents into smaller text chunks.

3\. Generate embeddings using Sentence Transformers.

4\. Store the text and embeddings in ChromaDB.

5\. Convert the user's question into an embedding.

6\. Retrieve relevant context through semantic similarity search.

7\. Apply a similarity threshold to filter weak matches.

8\. Pass the retrieved context and question to the local LLM.

9\. Generate a context-based answer or return a fallback when relevant information is insufficient.

10\. Display the response in the Streamlit chat interface.



> This project is being developed incrementally, with a focus on building practical GenAI solutions using open-source technologies and following AI engineering best practices.

