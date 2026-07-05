# Personalized Academic Research Assistant

A research-oriented prototype for Conversational Information Retrieval and Retrieval-Augmented Generation over academic papers.

## Features

- PDF text extraction and chunking
- TF-IDF baseline retrieval
- Semantic search using Sentence Transformers
- Gemini-based query rewriting
- User memory and personalized ranking
- Answer generation grounded in retrieved passages
- Streamlit web interface
- Source display with paper name and page number

## Pipeline

User Query  
→ Gemini Query Rewriting  
→ Semantic Retrieval  
→ User Memory Personalization  
→ Answer Generation  
→ Sources and Retrieved Passages

## Setup

1. Create virtual environment:

- python -m venv venv

2. Activate environment:

- venv\Scripts\activate

3. Install requirements:

- pip install -r requirements.txt

4. Create .env file:

- GEMINI_API_KEY=your_api_key_here

5. Run the app:

- streamlit run app.py


