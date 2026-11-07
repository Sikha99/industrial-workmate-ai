
from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from orchestrator import process_request, resume_request


app = FastAPI(
    title="Industrial WorkMate AI",
    description="API for Factory Work Assistance",
    version="1.0.0"
)


# Store pending requests for each conversation
chat_sessions = {}


# Request model
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/")
def home():
    return {
        "message": "Industrial WorkMate AI API is running!"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # Get existing session ID or create a new one
    session_id = request.session_id or str(uuid4())

    # Check whether this conversation has a pending request
    pending_request = chat_sessions.get(session_id)

    if pending_request:
        result = resume_request(
            pending_request,
            request.message
        )
    else:
        result = process_request(request.message)

    # Save pending request if more details are required
    if isinstance(result, dict) and result.get("status") == "missing_details":
        chat_sessions[session_id] = result
    else:
        chat_sessions.pop(session_id, None)

    return {
        "status": "success",
        "session_id": session_id,
        "response": result
    }
