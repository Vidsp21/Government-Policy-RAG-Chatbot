import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from ingestion.loader import load_documents
from ingestion.splitter import split_documents
from ingestion.vector_store import build_vector_store

def run_ingestion():
    print("Starting ingestion...")
    
    # Load documents
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")
    
    if not documents:
        print("ERROR: No documents were loaded. Check your data directory.")
        return
    
    # Split documents
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    if not chunks:
        print("ERROR: No chunks were created. Check your splitting logic.")
        return
    
    # Build vector store
    build_vector_store(chunks)
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    run_ingestion()