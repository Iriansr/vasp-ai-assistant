# 🧠 VASP AI Assistant - GEMINI Context

This project is an AI-powered assistant for computational materials science, specifically designed to answer questions about **VASP** (Vienna Ab initio Simulation Package) workflows. It uses a hybrid architecture combining **Retrieval-Augmented Generation (RAG)** and **Web Search** orchestrated by **LangGraph**.

## 🏗️ Architecture & Core Technologies

- **Orchestration**: `LangGraph` handles the flow from user query to routing, tool execution (RAG or Web Search), and validation.
- **LLM**: `Vertex AI` (Google Gemini 2.0 Flash) is used for routing, generation, and validation.
- **Vector Database**: `Elasticsearch` stores and retrieves chunked VASP documentation.
- **Backend**: `FastAPI` provides a REST endpoint for the chat interface.
- **Frontend**: A custom HTML/CSS/JS interface for interacting with the assistant.

## 📁 Project Structure

- `api/`: FastAPI server and request/response schemas.
- `frontend/`: Static web interface.
- `graph/`: LangGraph orchestration logic and graph definitions.
- `llm/`: Integration with Vertex AI (Gemini).
- `nodes/`: Individual logic units for the LangGraph (Router, RAG, Web Search, Validator).
- `rag_vasp/`: Complete RAG pipeline including ingestion, retrieval, and reranking.
- `web_search/`: Web search integration and summarization logic.

## 🚀 Setup and Commands

### 1. Environment Setup
The project uses Conda for dependency management.
```bash
conda env create -f rag_vasp/environment.yml
conda activate vasp-rag
```

### 2. Infrastructure (Elasticsearch)
Elasticsearch must be running locally for the RAG system to work.
```bash
docker run -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0
```

### 3. Data Ingestion
Before the first run, ingest the VASP documentation into Elasticsearch:
```bash
python -m rag_vasp.ingestion_script
```

### 4. Running the Backend
Start the FastAPI server using Uvicorn:
```bash
uvicorn api.main:app --reload
```
The API runs at `http://127.0.0.1:8000`.

### 5. Running the Frontend
Serve the `frontend/` directory using a simple HTTP server:
```bash
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500` in your browser.

## 🛠️ Configuration & Environment Variables

The project uses Pydantic for configuration (`rag_vasp/config/settings.py`). Ensure the following environment variables are set:

- `VERTEX_PROJECT`: Your Google Cloud Project ID.
- `VERTEX_LOCATION`: Vertex AI region (default: `us-central1`).
- `ES_HOST`: Elasticsearch host URL (default: `http://127.0.0.1:9200`).

## 🧠 Development Conventions

- **State Management**: LangGraph state is managed as a simple dictionary (`GraphState`).
- **LLM Selection**: `gemini-2.0-flash-001` is preferred for low latency and high quality in reasoning tasks.
- **Routing Logic**: The system intelligently routes between `rag` (VASP-specific docs) and `web` (general science/fallback) based on query semantics.
- **Validation**: Every answer is passed through a validator node to check for hallucinations or quality issues before being returned to the user.
- **Surgical Updates**: When modifying the graph, ensure that node dependencies in `graph/setgraph.py` are updated accordingly.
