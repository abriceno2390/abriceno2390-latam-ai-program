# ingest_docs.py
import os
import glob
import json
import chromadb
from chromadb.utils import embedding_functions
from ollama import Client as OllamaClient

# Initialize Ollama client (for embeddings)
ollama = OllamaClient()

# Initialize Chroma persistent client
CHROMA_PATH = "chroma_store"
COLLECTION_NAME = "docs_collection"

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create or get collection
try:
    collection = client.get_collection(COLLECTION_NAME)
except ValueError:
    collection = client.create_collection(COLLECTION_NAME)

# Directory containing your documents
DOCS_DIR = "docs_to_ingest"  # change to your folder path
SUPPORTED_EXTENSIONS = ["*.txt", "*.md", "*.pdf"]

# Function to read text files (basic for .txt and .md)
def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# TODO: Add PDF reader if needed
def read_pdf_file(path):
    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Ingest documents
documents = []
metadatas = []
ids = []

for ext in SUPPORTED_EXTENSIONS:
    for filepath in glob.glob(os.path.join(DOCS_DIR, ext)):
        filename = os.path.basename(filepath)
        if ext in ["*.txt", "*.md"]:
            text = read_text_file(filepath)
        elif ext == "*.pdf":
            text = read_pdf_file(filepath)
        else:
            continue

        # Split text into chunks (simple split by 1000 chars)
        chunk_size = 1000
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            # Generate embeddings using Ollama
            embedding = ollama.embeddings(model="nomic-embed-text", prompt=chunk)["embedding"]
            
            # Save chunk, embedding, and metadata
            documents.append(chunk)
            metadatas.append({"source": filename, "chunk": i // chunk_size})
            ids.append(f"{filename}-{i // chunk_size}")

# Add all chunks to Chroma collection
collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=documents  # Chroma will use your Ollama embeddings
)

print(f"Ingested {len(documents)} document chunks into Chroma collection '{COLLECTION_NAME}'.")
