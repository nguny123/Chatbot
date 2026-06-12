import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import google.generativeai as genai
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- Configuration & Setup ---

# Initialize Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Dockerized Gemini Chatbot")

# Set up Rate Limiting Exception Handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS Configuration ---
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://127.0.0.1",
    "http://127.0.0.1:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the domains above
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---

class ChatRequest(BaseModel):
    message: str

# --- Business Logic ---

async def stream_gemini_response(user_message: str):
    """
    Generates chunks of text from Gemini API.
    """
    try:
        # Use gemini-1.5-flash for speed/efficiency or gemini-1.5-pro for reasoning
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Enable streaming
        response = model.generate_content(user_message, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Error: {str(e)}"

# --- Routes ---

@app.post("/chat")
@limiter.limit("10/minute") # Rate limit: 10 requests per minute per IP
async def chat_endpoint(request: Request, chat_req: ChatRequest):
    if not os.getenv("GEMINI_API_KEY"):
        raise HTTPException(status_code=500, detail="Gemini API Key not configured.")
    
    return StreamingResponse(
        stream_gemini_response(chat_req.message),
        media_type="text/plain"
    )

@app.get("/health")
def health_check():
    return {"status": "ok", "provider": "Gemini"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)