# Personalized Academic Research Assistant

A Personalized Academic Research Assistant built using **Conversational Information Retrieval (CIR)** and **Retrieval-Augmented Generation (RAG)**.

The system allows users to ask natural language questions about a collection of academic PDF papers and receive grounded answers supported by retrieved passages and source references.

---

## Features

- Academic PDF processing and chunking
- TF-IDF baseline retrieval
- Semantic search using Sentence Transformers
- Query rewriting using Google Gemini
- Conversational query rewriting with chat history
- User memory for personalized ranking
- Grounded answer generation
- Source citations with paper names and page numbers
- Interactive Streamlit web interface

---

## System Pipeline

```
User Query
      │
      ▼
Chat History
      │
      ▼
Query Rewriting (Gemini)
      │
      ▼
Semantic Retrieval
      │
      ▼
Personalized Ranking (User Memory)
      │
      ▼
Grounded Answer Generation
      │
      ▼
Final Answer + Sources + Retrieved Passages
```

---

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- Scikit-learn
- Google Gemini API
- PyMuPDF
- NumPy
- JSON

---

## Project Structure

```
.
├── app.py
├── pdf_loader.py
├── retriever.py
├── semantic_retriever.py
├── personalized_ranker.py
├── memory.py
├── gemini_query_rewriter.py
├── answer_generator.py
├── data/
│   ├── chunks.json
│   └── memory.json
├── papers/
├── requirements.txt
└── README.md
```

---

## How It Works

1. Academic PDF papers are loaded and split into text chunks.
2. Chunks are converted into semantic embeddings.
3. The user asks a question through the Streamlit interface.
4. Gemini rewrites the query into a clearer academic search query.
5. The semantic retriever retrieves the most relevant passages.
6. Retrieved passages are re-ranked using user memory.
7. Gemini generates a grounded answer using only the retrieved passages.
8. The system displays the answer, sources, and retrieval scores.

---

## Experiments

The project evaluates several retrieval settings:

- TF-IDF vs Semantic Retrieval
- Semantic Retrieval vs Query Rewriting
- Effect of User Memory
- Conversational Follow-up Questions

---

## Future Improvements

- Larger academic datasets
- Automatic user profile learning
- Quantitative evaluation (Precision@K, Recall@K, MRR, F1)
- Better long-term conversational memory
- Support for additional embedding models
- Improved dialogue state tracking

---

## Installation

Clone the repository:

```bash
git clone https://github.com/hala205205/Personalized-Academic-Research-Assistant.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Dataset

The prototype uses a small collection of academic papers related to:

- Retrieval-Augmented Generation (RAG)
- Conversational Information Retrieval
- Scientific Literature Chatbots
- Memory-enhanced Retrieval

---

## Authors

**Hala Alnajjar**

**Raghad Elserhy**

**Nagham Ziediah**

AI and Data Science Students

---

## License

This project was developed for educational and research purposes.
