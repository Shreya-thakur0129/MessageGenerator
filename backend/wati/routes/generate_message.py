from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Message Generation"])

class MessagePrompt(BaseModel):
    prompt: str

class MessageResponse(BaseModel):
    message: str

# Simple rule-based template generator (can be replaced with LLM integration)
def generate_whatsapp_message(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "diwali" in prompt_lower:
        return "Hello {name}, Diwali greetings! Wishing you joy, prosperity, and success this festive season. Namaste!"
    if "new year" in prompt_lower:
        return "Hello {name}, Happy New Year! Wishing you a wonderful year ahead filled with happiness and success."
    if "birthday" in prompt_lower:
        return "Hello {name}, Happy Birthday! Wishing you a fantastic day and a year full of joy."
    # Default template
    return f"Hello {{name}}, {prompt.strip().capitalize()}"

@router.post("/generate-message", response_model=MessageResponse)
async def generate_message(data: MessagePrompt):
    if not data.prompt or not data.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    message = generate_whatsapp_message(data.prompt)
    return {"message": message}
