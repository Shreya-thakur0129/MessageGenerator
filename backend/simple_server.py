from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import csv
import io

app = FastAPI()

# Configure CORS to allow requests from your Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://messagegenerator.netlify.app",
        "https://www.messagegenerator.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class MessagePrompt(BaseModel):
    prompt: str

class MessageResponse(BaseModel):
    message: str

class Contact(BaseModel):
    name: Optional[str] = None
    phone: str

class Group(BaseModel):
    id: str
    name: str
    contacts: List[Contact]

class BroadcastRequest(BaseModel):
    message: str
    recipients: dict
    type: str

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

@app.get("/")
async def root():
    return {"status": "WhatsApp Message Generator API is running"}

@app.post("/generate-message")
async def generate_message(data: MessagePrompt):
    if not data.prompt or not data.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    message = generate_whatsapp_message(data.prompt)
    return {"message": message}

# Mock data for groups
MOCK_GROUPS = [
    Group(
        id="1",
        name="Regular Customers",
        contacts=[
            Contact(name="John Doe", phone="+1234567890"),
            Contact(name="Jane Smith", phone="+0987654321")
        ]
    ),
    Group(
        id="2",
        name="VIP Clients",
        contacts=[
            Contact(name="Alice Johnson", phone="+1122334455"),
            Contact(name="Bob Wilson", phone="+5544332211")
        ]
    )
]

@app.get("/groups")
async def get_groups():
    """Get all available contact groups"""
    return MOCK_GROUPS

@app.post("/broadcast-message")
async def broadcast_message(request: BroadcastRequest):
    """Broadcast a message to selected recipients"""
    try:
        recipients = []
        
        if request.type == "db":
            # Get contacts from selected group
            group_id = request.recipients.get("groupId")
            group = next((g for g in MOCK_GROUPS if g.id == group_id), None)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")
            recipients = group.contacts
        
        elif request.type == "upload":
            # Process uploaded file
            file_data = request.recipients.get("file")
            if not file_data:
                raise HTTPException(status_code=400, detail="No file provided")
            
            # In a real implementation, you would process the file here
            # For now, we'll return a success message
            return {"status": "success", "message": "File processed successfully"}
        
        elif request.type == "paste":
            # Process pasted numbers
            numbers = request.recipients.get("numbers", [])
            recipients = [Contact(phone=number) for number in numbers]
        
        else:
            raise HTTPException(status_code=400, detail="Invalid recipient type")
        
        # In a real implementation, you would send the messages here
        # For now, we'll return a success message with the count
        return {
            "status": "success", 
            "message": f"Message queued for {len(recipients)} recipients"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))