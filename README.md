# 🧠 VASP AI Assistant

An AI-powered assistant for computational materials science, designed to answer questions about VASP workflows using a hybrid **RAG + Web Search agent system**.

The system combines:
- 📚 Retrieval-Augmented Generation (RAG) over curated VASP documentation  
- 🌐 Web search fallback for broader queries  
- 🧠 LLM reasoning with validation and routing  
- 💬 Custom chat interface with Markdown 
---

## 🚀 Features

- 🔀 Intelligent router between **RAG** and **Web Search**
- 📖 Domain-specific knowledge (VASP, DFT, surface science)
- 🧪 Answer validation to prevent hallucinations
- 🔁 Controlled fallback (no infinite loops)
- 💬 Chat UI with:
  - Markdown rendering (`**bold**`, lists, etc.)
  - LaTeX equations (`$...$`, `$$...$$`)
- 🎨 Custom frontend UI

---

## 📁 Project Structure
```
full_agents/
│
├── rag_vasp/           # RAG pipeline (retriever, reranker, ingestion)
├── web_search/         # Web search agent
├── nodes/              # Graph nodes (router, rag, web, validator)
├── graph/              # LangGraph orchestration
├── api/                # FastAPI backend
├── frontend/           # Chat UI (HTML/CSS/JS)
└── README.md
```
---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vasp-ai-assistant.git
cd vasp-ai-assistant
```

### 2. Create envrionment

```bash
conda env create -f environment.yml
conda activate vasp-rag
```

### 3. Run data ingestion (RAG)

Before running the system, we gotta ingest the VASP docu into our database:

```bash
python -m rag_vasp.ingestion_script
```

This will: 
- Load the VASP docus.
- Chunk & embed them.
- Store them in a vector database (elasticsearch).

### 4. Elasticrun setup 

For the elastic search setup, make sure elasticsearch is running locally:

```bash
docker run -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.11.0
```

### 5. Run backend

Start the FastAPI server:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### 6. Run the frontend

Open the chat interface:
```bash
frontend/index.html
```

Or run a local server:
```bash
cd frontend
python -m http.server 5500
```
then open `http://localhost:5500`

---
### System flow

User Query
   ↓
Router (RAG vs Web)
   ↓
Tool (RAG or Web)
   ↓
Validator (checks answer quality)
   ↓
Optional fallback → Web
   ↓
Final Answer

---
 
🧪 Example Queries
	•	How to compute surface energy in VASP?
	•	What is a k-point mesh?
	•	How to run a band structure calculation?

---

 🧠 Tech Stack
	•	LLM: Vertex AI (Gemini)
	•	Backend: FastAPI
	•	Orchestration: LangGraph
	•	Vector DB: Elasticsearch
	•	Frontend: HTML / CSS / JS

---
⚠️ Notes
	•	Ensure Vertex AI credentials are properly configured
	•	Elasticsearch must be running before ingestion
	•	First ingestion may take several minutes

---

📌 Future Improvements
	•	Streaming responses (real-time typing)
	•	Multi-turn memory
	•	Better reranking strategies
	•	Deployment (Docker / cloud)





