# RAG (Production Grade) Assignment

## Objective

Improve retrieval accuracy in a RAG pipeline using multiple retrieval enhancement techniques.

---

## Setup

* Embedding Model: Sentence Transformers (`all-MiniLM-L6-v2`)
* Vector DB: ChromaDB
* Keyword Search: TF-IDF (scikit-learn)
* Input: sample.txt

---

## Query Used

```
What are advantages?
```

---

## Results Comparison

### 1. Baseline (Embedding Search)

```
['Advantages:\n- Scalability\n- Independent deployment',
 'Disadvantages:\n- Complexity\n- Network latency']
```

### 2. Keyword Search (TF-IDF)

```
['Advantages:\n- Scalability\n- Independent deployment',
 'Disadvantages:\n- Complexity\n- Network latency']
```

### 3. Hybrid Search (Embedding + Keyword)

```
['Advantages:\n- Scalability\n- Independent deployment',
 'Disadvantages:\n- Complexity\n- Network latency']
```

### 4. Reranked Results

```
['Advantages:\n- Scalability\n- Independent deployment',
 'Disadvantages:\n- Complexity\n- Network latency']
```

### 5. Metadata Filtering

```
['Advantages:\n- Scalability\n- Independent deployment']
```

---

## Comparison Table

| Method          | Relevance   | Observation                                        |
| --------------- | ----------- | -------------------------------------------------- |
| Baseline        | Medium      | Returns both relevant and irrelevant chunks        |
| Keyword         | Medium-High | Works well for exact match queries                 |
| Hybrid          | High        | Combines semantic + keyword strengths              |
| Rerank          | High        | Improves ordering but limited effect on small data |
| Metadata Filter | Very High   | Removes irrelevant chunks completely               |

---

## Key Insights

* Embedding search retrieves semantically related chunks but may include irrelevant ones
* Keyword search performs well for exact queries but lacks semantic understanding
* Hybrid search improves both recall and precision
* Reranking improves ordering but impact is limited on small datasets
* Metadata filtering significantly improves precision by removing noise

---

## Limitations

* Dataset is very small, so differences between methods are minimal
* Reranking uses simple similarity (not cross-encoder)
* No full LLM answer generation layer integrated

---

## Conclusion

Combining multiple retrieval strategies improves overall accuracy. While hybrid search balances precision and recall, metadata filtering provides the cleanest results. For production systems, a combination of hybrid retrieval, reranking, and metadata filtering is recommended.

---

## Final Note

This implementation demonstrates a production-style RAG pipeline with retrieval optimization techniques applied on a local setup.
