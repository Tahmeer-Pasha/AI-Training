# AI Assignments – LLM & RAG Experiments

## Overview
This repository contains experiments on:
- LLM decoding behavior
- Prompt engineering techniques
- RAG (Retrieval-Augmented Generation)

---

## 1. Decoding Experiment
Analyzed how LLM outputs vary across multiple runs and prompt variations.

---

## 2. Prompt Engineering
Implemented:
- Zero-shot prompting
- Few-shot prompting
- Role-based prompting
- Structured JSON outputs

---

## 3. RAG Pipeline
Built a basic RAG system using:
- Sentence Transformers (embeddings)
- ChromaDB (vector storage)

Compared chunking strategies:
- Fixed chunking
- Overlapping chunks
- Semantic chunking

---

## Key Insight
Semantic chunking provided the most relevant results, while overlapping chunks improved recall.

---

## Tech Stack
- Python
- Ollama (LLM)
- Sentence Transformers
- ChromaDB