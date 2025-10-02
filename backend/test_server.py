from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessagePrompt(BaseModel):
    prompt: str

class MessageResponse(BaseModel):
    message: str

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

@app.post("/generate-message", response_model=MessageResponse)
async def generate_message(data: MessagePrompt):
    message = generate_whatsapp_message(data.prompt)
    return {"message": message}