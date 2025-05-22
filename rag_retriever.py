from sentence_transformers import SentenceTransformer
import faiss
import pickle

def retrieve_relevant_chunks(query, top_k=2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("schema_index.faiss")

    with open("schema_docs.pkl", "rb") as f:
        documents = pickle.load(f)

    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, top_k)
    return [documents[i] for i in I[0]]

def build_prompt(context_chunks, user_question):
    return f"""You are an expert SQL assistant.

Here is the database schema:
{chr(10).join(context_chunks)}

Write a SQL query to answer this question:
{user_question}
"""
