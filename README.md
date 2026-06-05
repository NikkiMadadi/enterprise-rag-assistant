# Enterprise Multi-Document RAG Assistant

A local Retrieval-Augmented Generation (RAG) application that allows users to upload multiple PDF documents and ask questions across them.

## Features

- Multi-document PDF upload
- PDF text extraction using PyPDF
- Text chunking with overlap
- Embedding generation using Sentence Transformers
- Vector storage and semantic search using ChromaDB
- Local LLM response generation using Ollama and Llama 3.1
- Source document display for retrieved chunks
- Multi-document summarization support

## Architecture

PDF Upload  
→ Text Extraction  
→ Chunking  
→ Embedding Generation  
→ ChromaDB Vector Store  
→ Semantic Retrieval  
→ Llama 3.1 via Ollama  
→ Answer with Sources

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Sentence Transformers
- PyPDF
- Ollama
- Llama 3.1

## How to Run

1. Create virtual environment

```bash
python -m venv venv