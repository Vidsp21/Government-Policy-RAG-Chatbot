import os
from langchain_community.document_loaders import PyPDFLoader
from config import DATA_DIR

def load_documents():
    documents = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, file)
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file

            documents.extend(docs)

    return documents
