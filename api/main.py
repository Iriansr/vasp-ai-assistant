import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="google.api_core.*")

from fastapi import FastAPI
from api.schemas import ChatRequest, ChatResponse
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions.sqlite_session_service import SqliteSessionService
from orchestration import vasp_ai_assistant
from google.genai import types

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en dev está ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ADK Runner with Persistent SQLite Session
session_service = SqliteSessionService(db_path="sessions.db")
runner = Runner(
    app_name="vasp_assistant",
    agent=vasp_ai_assistant,
    session_service=session_service,
    auto_create_session=True
)


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=request.query)]
    )

    final_answer = ""
    sources = []

    # Run the assistant and collect events
    async for event in runner.run_async(
        user_id="anonymous_user",
        session_id=request.session_id or "default_fallback_session",
        new_message=user_message
    ):
        # Extract text from events
        if event.content:
            for part in event.content.parts:
                if part.text:
                    final_answer += part.text

        # Extract sources from tool outputs
        for fr in event.get_function_responses():
            if isinstance(fr.response, dict) and "sources" in fr.response:
                for s in fr.response["sources"]:
                    sources.append({
                        "title": s.get("title") or s.get("section") or "Source",
                        "url": s.get("url") or "#"
                    })

    return {
        "answer": final_answer.strip(),
        "sources": sources,
        "route": "adk_orchestration"
    }