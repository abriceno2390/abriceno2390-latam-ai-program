import requests
import json
import chromadb
import argparse
import difflib

# --- 1. Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/api"
OLLAMA_CONFIG = {
    "model": "llama3",
    "stream": False,
}
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "faq_collection"

# --- 2. Knowledge Base ---
# In a real-world scenario, this would come from a file, database, or API.
FAQ_DATA = [
    {"id": "faq1", "question": "What is the return policy?", "answer": "You can return any item within 30 days of purchase for a full refund."},
    {"id": "faq2", "question": "How do I track my order?", "answer": "Once your order has shipped, you will receive an email with a tracking number."},
    {"id": "faq3", "question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide. Shipping costs may vary."},
    {"id": "faq4", "question": "How can I contact customer support?", "answer": "You can reach our customer support team via email at support@example.com or by calling our toll-free number."},
    {"id": "faq5", "question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and Apple Pay."},
    {"id": "faq6", "question": "Can I change my shipping address?", "answer": "If your order has not yet shipped, you can contact customer support to update your shipping address."},
    {"id": "faq7", "question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, from 9 AM to 5 PM EST."},
    {"id": "faq8", "question": "Do you offer gift wrapping?", "answer": "Yes, we offer gift wrapping for an additional fee. You can select this option at checkout."},
    {"id": "faq9", "question": "How do I use a discount code?", "answer": "You can apply your discount code in the 'Promo Code' box at checkout."},
    {"id": "faq10", "question": "What if my item is damaged?", "answer": "If your item arrives damaged, please contact customer support immediately for a replacement or refund."}
]



# --- 3. ChromaDB Setup ---
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- 4. Helper Functions ---

#-------Argparse code----------------------------------------------------------------------------------------------------------------------------------------



def get_cli_args():
    """
    Parses CLI arguments for RAG script.
    Returns:
        queries: list of query strings
        k: top number of results to retrieve
        use_context: whether to use context (False if --no-context is set)
    """
    parser = argparse.ArgumentParser(description="RAG script options")

    # Queries
    parser.add_argument('--query', type=str, help='Single query string')
    parser.add_argument('--queries-file', type=str, help='File with multiple queries, one per line')

    # Top k
    parser.add_argument('--k', type=int, default=5, help='Number of top documents to retrieve')

    # Context flag
    parser.add_argument('--no-context', action='store_true', help='Ignore context if set')

    # parse_known_args allows other parts of the script to still parse CLI args
    args, unknown = parser.parse_known_args()

    # Prepare queries
    if args.queries_file:
        try:
            queries = [line.strip() for line in open(args.queries_file) if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {args.queries_file} not found.")
            exit(1)
    elif args.query:
        queries = [args.query]
    else:
        # fallback to old hard-coded queries
        queries = [
            "How can I return a product?",
            "What's the process for tracking my package?",
            "Do you ship to Canada?",
            "What are the support hours?",
            "Can I pay with Bitcoin?"
        ]

    k = args.k
    use_context = not args.no_context

    return queries, k, use_context



#-------Argparse code ends-----------------------------------------------------------------------------------------------------------------------------------



def get_embedding(text):
    """
    Generates an embedding for the given text using the Ollama API.
    """
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/embeddings",
            json={"model": OLLAMA_CONFIG["model"], "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding: {e}")
        return None

def index_knowledge_base():
    """
    Indexes the knowledge base into ChromaDB.
    """
    print("Indexing knowledge base...")
    for item in FAQ_DATA:
        # We are embedding the questions to find similar user queries.
        embedding = get_embedding(item["question"])
        if embedding:
            collection.add(
                ids=[item["id"]],
                embeddings=[embedding],
                documents=[item["answer"]],  # Store the answer as the document
                metadatas=[{"question": item["question"]}]
            )
    print("Indexing complete.")


#def retrieve_documents(query, top_k=5):
 #   """
  #  Retrieve up to top_k matching documents from FAQ_DATA based on query.
   # """
    #matches = [
     #   faq for faq in FAQ_DATA
      #  if query.lower() in faq['question'].lower() or query.lower() in faq['answer'].lower()
    #]
    #return matches[:top_k]    

def query_rag_agent(user_query, top_k, use_context):
    """
    Queries the RAG agent with a user's question.
    """
    print(f"\n--- Querying for: '{user_query}' ---")
    print(f"(use_context={use_context}, top_k={top_k})")
    
    # 1. Get embedding for the user query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Sorry, I couldn't process your query."

    # 2. Query ChromaDB for relevant context
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k  # Retrieve the top 2 most relevant documents

 


    )
    





    if use_context:
         if results.get('documents') and results['documents'][0]:
        #if results['documents']:
            context_blocks = []
            citations = []

            docs = results['documents'][0]
            ids = results.get('ids',[[]])[0] if 'ids' in results else []
            metas = results.get('metadatas', [[]])[0] if 'metadatas' in results else []


            for i, doc in enumerate(docs, start=1):
                source_id = ids[i-1] if i-1 < len(ids) else f"source_{i}"
                source_meta = metas[i-1] if i-1 < len(metas) else {}


                block = (
                          f"---CONTEXT BLOCK {i}---\n"
                          f"{doc}\n"
                          f"---END CONTEXT BLOCK {i}---"
                )
                context_blocks.append(block)
                
                if source_meta and 'title' in source_meta:
                  citations.append(f"[{i}] {source_meta['title']}")
                else:
                  citations.append(f"[{i}] {source_id}")

            context_block = "\n\n".join(context_blocks)
            
            citations_text = "\n".join(citations)
            citation_section = f"\n\nCitations:\n{citations_text}"
         else:
            context_block = "---CONTEXT BLOCK 1---\nNo relevant information found.\n---END CONTEXT BLOCK 1---"
            citation_section = "\n\nCitations:\nNone available"

         print(f"Retrieved context:\n{context_block}") 
         print(f"\n{citation_section}")
    else:
         context_block = "------Context Block------\nNo No Context provided.\n---END CONTEXT BLOCK 1---"
         print("Context skipped due to --no-context")
         citation_section = "\n\nNone (context disabled)" 
         print(f"\n{citation_section}")
         
         
    
         


     
    #retrieved_context = "\n".join(results['documents'][0]) if results['documents'] else "No relevant information found."
    
    #print(f"Retrieved context: {retrieved_context}")

    # 3. Construct the prompt for the LLM
    prompt = f"""
    You are a helpful FAQ assistant. A user has asked the following question:
    '{user_query}'

    Here is some context that might be relevant:
    '{context_block}' 
        


    Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
    """

    # 4. Send the prompt to the LLM
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()
        return json.loads(response.text)["response"]
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

# --- 5. Main Execution ---
if __name__ == "__main__":
    # Check if the collection is empty before indexing
    if collection.count() == 0:
        index_knowledge_base()
    else:
        print("Knowledge base is already indexed.")

    queries, k, use_context = get_cli_args()

    # --- Test Queries ---
   # test_queries = [
    #    "How can I return a product?",
     #   "What's the process for tracking my package?",
      #  "Do you ship to Canada?",
       # "What are the support hours?",
        #"Can I pay with Bitcoin?" # A question not in the knowledge base
    #]
    
    print(f"use_context={use_context}, top_k={k}")

    for query in queries:
        answer = query_rag_agent(query, top_k=k, use_context=use_context)
        print(f"Answer: {answer}")
