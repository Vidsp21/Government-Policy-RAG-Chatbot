import chromadb
from config import VECTOR_DB_DIR

# Connect to ChromaDB
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

# Get collection
collection = client.get_collection(name="langchain")

# Get embeddings with metadata
results = collection.get(
    limit=5,  # Get first 5 items
    include=["embeddings", "documents", "metadatas"]
)

print(f"Total vectors: {collection.count()}\n")

for i, (doc, embedding, metadata) in enumerate(zip(
    results['documents'], 
    results['embeddings'], 
    results['metadatas']
)):
    print(f"--- Document {i+1} ---")
    print(f"Source: {metadata.get('source', 'N/A')}")
    print(f"Page: {metadata.get('page', 'N/A')}")
    print(f"Text preview: {doc[:100]}...")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 10 values: {embedding[:10]}")
    print(f"Vector norm: {sum(x**2 for x in embedding)**0.5:.4f}")
    print()