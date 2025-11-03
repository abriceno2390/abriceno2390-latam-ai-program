from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from ollama import Client as OllamaClient
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Docs-to-Answers RAG Assistant")

# Initialize Ollama client
ollama = OllamaClient()

# Chroma configuration
CHROMA_PATH = "chroma_store"
COLLECTION_NAME = "docs_collection"

try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
except Exception as e:
    raise RuntimeError(f"Failed to connect to Chroma: {e}")

# Request body schema
class QueryRequest(BaseModel):
    query: str
    k: int = 3  # number of chunks to retrieve

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        # Step 1: Create embeddings for the query
        query_embedding = ollama.embeddings(
            model="nomic-embed-text",
            prompt=request.query
        )["embedding"]

        # Step 2: Retrieve relevant documents from Chroma
        results = collection.query(query_embeddings=[query_embedding], n_results=request.k)

        if not results["documents"][0]:
            raise HTTPException(status_code=404, detail="No matching documents found.")

        # Step 3: Prepare context and citations
        context = ""
        citations = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context += f"{doc}\n"
            citations.append(f"({meta['source']}#{meta['chunk']})")

        # Step 4: Ask the chat model using retrieved context
        prompt = f"""You are a helpful assistant. Use the context below to answer the question.
Include citations in the format (source#chunk).

Context:
{context}

Question: {request.query}
Answer:"""

        response = ollama.chat(
            model="phi",  # CPU-friendly small model
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "answer": response["message"]["content"],
            "citations": citations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
