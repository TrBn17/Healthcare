from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from core.gemini_call import chat_with_gemini, chat_with_gemini_stream
import json

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    stream: bool = False

@router.post("/chat")
def chat(request: ChatRequest):
    if request.stream:
        def generate():
            for chunk in chat_with_gemini_stream(request.message):
                yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(generate(), media_type="text/event-stream")
    else:
        return chat_with_gemini(request.message)
