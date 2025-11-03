import argparse
import os
import ollama
import chromadb
from chromadb.config import Settings

# ---- Configuration ----
CHROMA_PERSIST_DIR = "./chroma_store"
COLLECTION_NAME = "docs_collection"
MODEL = "nomic-embed-text"

# ---- Parse CLI arguments ----
parser = argparse.ArgumentParser(description="Query local documents using Ollama + ChromaDB")
parser.add_argument("--query", type=str, required=True, help="The question or search text")
parser.add_argument("--k", type=int, default=3, help="Number of similar documents to retrieve")
args = parser.parse_args()

# ---- Initialize Chroma client ----
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

# ---- Load or verify collection ----
try:
    collection = client.get_collection(COLLECTION_NAME)
except Exception as e:
    raise RuntimeError(f"❌ Collection '{COLLECTION_NAME}' not found. "
                       f"Make sure you’ve already run your document loader first!") from e

# ---- Embed the query using Ollama ----
print(f"🔹 Generating embedding with Ollama model '{MODEL}'...")
query_embedding = ollama.embeddings(model=MODEL, prompt=args.query)["embedding"]

# ---- Query ChromaDB ----
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=args.k
)

# ---- Print results ----
print("\n🔍 Top matches:")
for i, doc in enumerate(results["documents"][0]):
    print(f"\n📄 Document {i+1}:")
    print(doc)
    print("-" * 60)
