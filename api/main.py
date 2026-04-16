import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.api_core.*")

from fastapi import FastAPI
from api.schemas import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware

from graph.setgraph import build_graph

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en dev está ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load graph one time 
graph = build_graph()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = graph.invoke({
        "query": request.query
    })

    # normalize sources
    sources = [
        {
            "title": s.get("title"),
            "url": s.get("url")
        }
        for s in result.get("sources", [])
    ]

    return {
        "answer": result.get("answer", ""),
        "sources": sources,
        "route": result.get("route")
    }