# AI Assignments – LLM & RAG Experiments

## 🚀 Overview
This repository contains hands-on experiments exploring core concepts in modern AI systems:

- LLM decoding behavior (determinism vs creativity)
- Prompt engineering techniques
- Retrieval-Augmented Generation (RAG)
- Production-grade retrieval improvements

The goal is to understand how LLMs behave and how retrieval quality can be improved in real-world systems.

---

## 🧠 1. Decoding Experiment
Analyzed how LLM outputs vary across multiple runs and prompt variations.

### Key Learnings:
- LLM outputs are non-deterministic by default
- Prompt phrasing affects response structure
- Tradeoff:
  - Low randomness → consistent outputs (good for APIs)
  - High randomness → creative outputs

---

## ✍️ 2. Prompt Engineering
Implemented multiple prompting techniques:

- Zero-shot prompting
- Few-shot prompting
- Role-based prompting
- Structured JSON output

### Key Learnings:
- Few-shot improves consistency
- Role prompting improves clarity and usefulness
- Structured outputs are critical for backend integration

---

## 🔎 3. RAG Pipeline (Fundamentals)

Built a basic Retrieval-Augmented Generation pipeline using:

- Sentence Transformers (embeddings)
- ChromaDB (vector database)

### Chunking Strategies Compared:
- Fixed chunking
- Overlapping chunks
- Semantic chunking

### Key Insight:
- Semantic chunking provided the most relevant results
- Overlapping improved recall but added redundancy

---

## ⚙️ 4. RAG (Production Grade Improvements)

Enhanced retrieval accuracy by implementing:

- Keyword search (TF-IDF)
- Hybrid retrieval (embedding + keyword)
- Reranking (similarity-based)
- Metadata filtering

### Key Insights:
- Keyword search improves precision for exact queries
- Embeddings capture semantic meaning
- Hybrid search balances precision and recall
- Reranking improves ordering of results
- Metadata filtering significantly improves relevance

### Limitation:
Due to small dataset size, differences between methods are subtle. However, these techniques scale effectively for larger datasets.

---

## 📊 Overall Learnings

- Retrieval quality is as important as the LLM itself
- Chunking strategy directly impacts RAG performance
- Combining retrieval techniques gives better results than using one alone
- Production systems require hybrid + reranking approaches

---

## 🛠️ Tech Stack

- Python
- Ollama (Local LLM)
- Sentence Transformers
- ChromaDB
- Scikit-learn (TF-IDF)

---

## 📌 Future Improvements

- Integrate LLM (Ollama) for final answer generation
- Use cross-encoder for advanced reranking
- Add larger and real-world datasets
- Build API layer (Spring Boot / FastAPI)

---
## 💡 Summary

This project demonstrates the evolution from basic LLM usage to building a production-aware RAG pipeline with improved retrieval strategies.