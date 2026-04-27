# RAG Fundamentals Assignment

## Objective

Build a basic Retrieval-Augmented Generation (RAG) pipeline and compare different chunking strategies.

---

## Setup

* Embedding Model: `all-MiniLM-L6-v2` (Sentence Transformers)
* Vector DB: Chroma
* Input: `sample.txt`

---

## Input Document

```
Microservices architecture allows applications to be divided into small independent services.

Advantages:
- Scalability
- Independent deployment

Disadvantages:
- Complexity
- Network latency
```

---

## Pipeline Steps

1. Load document
2. Split into chunks
3. Generate embeddings
4. Store in vector DB
5. Query relevant chunks

---

## Query Used

```
What are advantages?
```

---

## Retrieved Outputs

### Fixed Chunking

```
[['Microservices architecture allows applications to be divided into small independent services.

Advantages:
- Scalability
- Independent deployment

Disadvantages:
- Complexity
- Network latency']]
```

### Overlap Chunking

```
[['advantages:
- Complexity
- Network latency',
  'Microservices architecture allows applications to be divided into small independent services.

Advantages:
- Scalability
- Independent deployment

Disadvantages:
- Complexity
- Network latency']]
```

### Semantic Chunking

```
[['Advantages:
- Scalability
- Independent deployment',
  'Disadvantages:
- Complexity
- Network latency']]
```

---

## Chunking Strategies Comparison

### 1. Fixed Chunking (No Overlap)
- Chunk Size: 200
- Overlap: 0

**Observation:**
- Retrieved partial context
- Some related info may be split across chunks

---

### 2. Overlapping Chunking
- Chunk Size: 200
- Overlap: 50

**Observation:**
- Better context retention
- Higher chance of retrieving complete information

---

### 3. Semantic Chunking (Paragraph Split)
- Split by `\n\n`

**Observation:**
- Most relevant chunks retrieved
- Logical grouping improves accuracy

---

## Comparison Table

| Strategy | Relevance | Context Retention | Quality |
|----------|----------|------------------|--------|
| Fixed | Medium | Low | OK |
| Overlap | High | Medium | Better |
| Semantic | Very High | High | Best |

---

## Key Insights

- Fixed chunking is simple but may lose context
- Overlapping chunks improve recall
- Semantic chunking provides best relevance by preserving meaning

---

## Conclusion

Chunking strategy significantly impacts RAG performance. For simple use cases, overlapping chunks offer a good balance. For higher accuracy, semantic chunking is preferred.

---

## Final Note

This implementation uses a local embedding model and vector database to simulate a real-world RAG pipeline.

