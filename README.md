# Government Policy RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about Indian government policies and acts. The system uses semantic search to retrieve relevant policy documents and generates accurate answers using a local LLM (Ollama).

## 📋 Features

- **Document Processing**: Automatically loads and processes PDF policy documents
- **Semantic Search**: Uses sentence transformers for intelligent document retrieval
- **Local LLM**: Powered by Ollama (Phi model) for privacy and offline capability
- **Vector Database**: ChromaDB for efficient similarity search
- **Web Interface**: Clean Flask-based UI for easy interaction
- **CLI Interface**: Command-line tool for quick queries
- **Source Attribution**: Shows relevant document excerpts with each answer
- **Performance Metrics**: Displays retrieval and generation times

## 📚 Included Policy Documents

The system currently includes knowledge about:
- **Education**: Intermediate Education Act, 1921 (Uttar Pradesh)
- **Healthcare**: Health Workers and Health Supervisors (Regulation of Pay) Act, 1996
- **Mental Health**: Mental Healthcare Act, 2017
- **Traffic**: 
  - Immoral Traffic (Prevention) Act, 1956
  - Karnataka Traffic Control Act, 1960
  - Control of National Highways (Land and Traffic) Act, 2002
- **Housing**: Rent Agreement regulations

## 🛠️ Technology Stack

- **Framework**: LangChain for RAG orchestration
- **Vector Store**: ChromaDB with cosine similarity
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: Ollama (Phi model)
- **PDF Processing**: PyPDF
- **Web Framework**: Flask
- **Frontend**: HTML/CSS/JavaScript

## 📦 Installation

### Prerequisites

1. **Python 3.8+**
2. **Ollama**: Install from [ollama.ai](https://ollama.ai)
   ```bash
   # Pull the Phi model
   ollama pull phi
   ```

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd C:\Users\HP\Documents\1 PROJECTS\GOV-CHATBOT
   cd gov-policy-rag
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv rag-env
   ```

3. **Activate the virtual environment**
   ```bash
   # Windows
   .\rag-env\Scripts\Activate.ps1
   
   # Linux/Mac
   source rag-env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the ingestion pipeline** (First time only or when adding new documents)
   ```bash
   python scheduler/ingest_job.py
   ```
   This will:
   - Load all PDF documents from `data/policies/`
   - Split them into chunks
   - Generate embeddings
   - Store vectors in ChromaDB

## 🚀 Usage

### Web Interface (Recommended)

1. **Start the Flask server**
   ```bash
   python app_web.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

3. **Ask questions** about government policies!

### Command Line Interface

```bash
python app.py
```

Then type your question when prompted.

## 📁 Project Structure

```
gov-policy-rag/
├── app.py                      # CLI application
├── app_web.py                  # Flask web application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── view_embeddings.py          # Utility to inspect vector DB
│
├── data/
│   └── policies/               # PDF policy documents
│       ├── education 1.pdf
│       ├── health workers.pdf
│       ├── mental health 1.pdf
│       ├── mental health 2.pdf
│       ├── rent agreement 1.pdf
│       ├── traffic 1.pdf
│       ├── traffic 2.pdf
│       └── traffic 3.pdf
│
├── ingestion/                  # Document processing pipeline
│   ├── __init__.py
│   ├── loader.py              # PDF document loader
│   ├── splitter.py            # Text chunking
│   └── vector_store.py        # ChromaDB operations
│
├── query/                      # RAG query pipeline
│   ├── __init__.py
│   ├── retriever.py           # Semantic search
│   └── rag_chain.py           # LLM answer generation
│
├── scheduler/                  # Batch processing
│   ├── __init__.py
│   └── ingest_job.py          # Document ingestion script
│
├── templates/                  # Web UI templates
│   └── index.html
│
├── vector_db/                  # ChromaDB storage (generated)
└── rag-env/                    # Virtual environment
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Paths
DATA_DIR = "data/policies"          # Source PDF directory
VECTOR_DB_DIR = "vector_db"         # Vector database location

# Models
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "phi"                   # Ollama model name

# Chunking
CHUNK_SIZE = 600                    # Characters per chunk
CHUNK_OVERLAP = 100                 # Overlap between chunks

# Retrieval
TOP_K = 5                           # Number of documents to retrieve
```

## 🔍 Example Queries

Try asking questions like:

**Education:**
- "What is the Intermediate Education Act of 1921?"
- "Which amendments have been made to the education act?"

**Healthcare:**
- "What are the pay scales for health workers in Uttar Pradesh?"
- "What rights do persons with mental illness have?"

**Traffic:**
- "What is the Immoral Traffic Prevention Act?"
- "What are the duties of a driver in case of an accident?"

**Housing:**
- "What are the rights and obligations of landlords?"
- "How can a landlord evict a tenant?"

## 🧪 Testing Your RAG Model

Use the provided evaluation queries in the project documentation to:
- Test retrieval accuracy
- Measure answer precision
- Evaluate context understanding
- Check error handling for out-of-scope questions

## 🔄 Adding New Documents

1. Place PDF files in `data/policies/`
2. Run the ingestion script:
   ```bash
   python scheduler/ingest_job.py
   ```
3. The new documents will be processed and added to the vector database

## 🐛 Troubleshooting

**Issue: "No documents were loaded"**
- Check that PDF files exist in `data/policies/`
- Verify file permissions

**Issue: "Ollama connection error"**
- Ensure Ollama is running: `ollama serve`
- Verify the model is installed: `ollama list`
- Pull the model if missing: `ollama pull phi`

**Issue: "Empty responses"**
- Run ingestion again: `python scheduler/ingest_job.py`
- Check vector database was created in `vector_db/`

**Issue: "Out of memory"**
- Reduce `CHUNK_SIZE` in config.py
- Use a smaller embedding model
- Decrease `TOP_K` retrieval count

## 📈 Performance Optimization

- **Faster responses**: Use a smaller LLM model (e.g., `tinyllama`)
- **Better accuracy**: Increase `TOP_K` for more context
- **Larger documents**: Increase `CHUNK_SIZE` and `CHUNK_OVERLAP`
- **GPU acceleration**: Configure sentence-transformers to use CUDA

## 🤝 Contributing

To extend this project:
1. Add more policy documents to `data/policies/`
2. Customize the system prompt in `query/rag_chain.py`
3. Enhance the web UI in `templates/index.html`
4. Implement query preprocessing/filtering

## 📝 License

This project is for educational and informational purposes. Policy documents remain property of their respective government authorities.

## 🙏 Acknowledgments

- Policy documents sourced from Indian government publications
- Built with LangChain, ChromaDB, and Ollama
- Embedding models from Hugging Face

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review the configuration settings
- Ensure all dependencies are installed correctly

---

**Note**: This system provides information based on the documents provided. Always verify critical information with official government sources.
