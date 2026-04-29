from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load text
with open("sample.txt", "r") as f:
    text = f.read()

# --------- CHANGE THIS VALUE ----------
CHUNK_TYPE = "semantic"  
# options: "fixed", "overlap", "semantic"
# -------------------------------------

def fixed_chunk(text, size=200):
    return [text[i:i+size] for i in range(0, len(text), size)]

def overlap_chunk(text, size=200, overlap=50):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+size])
        i += size - overlap
    return chunks

def semantic_chunk(text):
    return text.split("\n\n")

# Select chunking strategy
if CHUNK_TYPE == "fixed":
    chunks = fixed_chunk(text)
elif CHUNK_TYPE == "overlap":
    chunks = overlap_chunk(text)
else:
    chunks = semantic_chunk(text)

print(f"\n--- Using {CHUNK_TYPE} chunking ---")
print("Chunks:\n", chunks)

# ---------------- EMBEDDINGS ----------------
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = [model.encode(chunk) for chunk in chunks]

# Store in Chroma
client = chromadb.Client()
collection = client.create_collection(f"test_{CHUNK_TYPE}")

for i, emb in enumerate(embeddings):
    collection.add(
        ids=[str(i)],
        embeddings=[emb.tolist()],
        documents=[chunks[i]]
    )

# ---------------- KEYWORD SEARCH (TF-IDF) ----------------
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(chunks)

def keyword_search(query, top_k=2):
    query_vec = vectorizer.transform([query])
    scores = (tfidf_matrix @ query_vec.T).toarray().flatten()
    ranked = np.argsort(scores)[::-1]
    return [chunks[i] for i in ranked[:top_k]]

# ---------------- EMBEDDING SEARCH ----------------
def embedding_search(query, top_k=2):
    query_emb = model.encode(query)
    results = collection.query(query_embeddings=[query_emb.tolist()], n_results=top_k)
    return results["documents"][0]

# ---------------- HYBRID SEARCH ----------------
def hybrid_search(query, top_k=2):
    emb_results = embedding_search(query, top_k)
    key_results = keyword_search(query, top_k)

    combined = list(dict.fromkeys(emb_results + key_results))
    return combined[:top_k]

# ---------------- RERANKING ----------------
def rerank(query, docs):
    query_emb = model.encode(query)
    scores = []

    for doc in docs:
        doc_emb = model.encode(doc)
        score = np.dot(query_emb, doc_emb)
        scores.append(score)

    ranked = [doc for _, doc in sorted(zip(scores, docs), reverse=True)]
    return ranked

# ---------------- METADATA FILTERING ----------------
chunks_with_meta = [
    {
        "text": chunk,
        "type": "advantage" if "Advantage" in chunk else "other"
    }
    for chunk in chunks
]

def filter_chunks(type_filter):
    return [c["text"] for c in chunks_with_meta if c["type"] == type_filter]

# ---------------- QUERY TEST ----------------
query = "What are advantages?"

print("\n--- Baseline (Embedding) ---")
baseline = embedding_search(query)
print(baseline)

print("\n--- Keyword Search ---")
keyword = keyword_search(query)
print(keyword)

print("\n--- Hybrid Search ---")
hybrid = hybrid_search(query)
print(hybrid)

print("\n--- Reranked Results ---")
reranked = rerank(query, hybrid)
print(reranked)

print("\n--- Metadata Filter (advantage only) ---")
filtered = filter_chunks("advantage")
print(filtered)