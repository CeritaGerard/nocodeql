from sentence_transformers import SentenceTransformer
import faiss
import pickle

# Define your schema as human-readable sentences
documents = [
    "Table: users. Columns: id, name, email, signup_date",
    "Table: orders. Columns: id, user_id, product, amount, order_date",
    "orders.user_id is a foreign key referencing users.id"
]

# Load an embedding model (MiniLM is lightweight and free)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate vector embeddings for schema
embeddings = model.encode(documents)

# Store the vectors in FAISS
index = faiss.IndexFlatL2(len(embeddings[0]))
index.add(embeddings)

# Save FAISS index and raw documents
faiss.write_index(index, "schema_index.faiss")

with open("schema_docs.pkl", "wb") as f:
    pickle.dump(documents, f)

print("✅ RAG index built and saved successfully.")