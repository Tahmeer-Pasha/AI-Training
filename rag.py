from sentence_transformers import SentenceTransformer
import chromadb

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

# Embeddings
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

# Query
query = "What are advantages?"
query_emb = model.encode(query)

results = collection.query(query_embeddings=[query_emb.tolist()], n_results=2)

print("\nRetrieved:\n", results["documents"])