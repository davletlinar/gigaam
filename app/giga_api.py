from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gigaam # type: ignore
import os
import uvicorn
from typing import Optional

# Create FastAPI app
app = FastAPI(title="Audio Transcribation API")

# Define request model
class TranscriptionRequest(BaseModel):
    uid: str
    record: str

# Define response model
class TranscriptionResponse(BaseModel):
    uid: str
    status: str
    transcription: Optional[str] = None
    error: Optional[str] = None
    
# Get token from environment variable
token = os.getenv('HF_TOKEN')
if not token:
    raise ValueError("HF_TOKEN environment variable is not set")

os.environ["HF_TOKEN"] = token

# Load model at startup
model = gigaam.load_model("ctc")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(request: TranscriptionRequest) -> TranscriptionResponse:
    try:
        print('Processing:', request.uid)
        recognition_result = model.transcribe_longform(request.record)
        transcription_chunks = [utterance["transcription"] for utterance in recognition_result]
        transcription = " ".join(transcription_chunks)
        
        return TranscriptionResponse(
            uid=request.uid,
            status="success",
            transcription=transcription
        )

    except Exception as e:
        return TranscriptionResponse(
            uid=request.uid,
            status="error",
            transcription='Internal server error',
            error=str(e)
        )
        
@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("giga_api:app", host="0.0.0.0", port=1488, reload=False)
