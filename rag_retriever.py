from sentence_transformers import SentenceTransformer
import faiss
import pickle

def retrieve_relevant_chunks(query, top_k=2):
    # Load the same embedding model and previously saved index
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("schema_index.faiss")
    
    # Load your original schema documents
    with open("schema_docs.pkl", "rb") as f:
        documents = pickle.load(f)
    
    # Embed the user's question
    query_embedding = model.encode([query])
    
    # Perform similarity search
    D, I = index.search(query_embedding, top_k)
    return [documents[i] for i in I[0]]

def build_prompt(context_chunks, user_question):
    return f"""You are an SQL assistant.
Here is the database schema:
{chr(10).join(context_chunks)}

Write a SQL query to answer this question:
{user_question}
"""