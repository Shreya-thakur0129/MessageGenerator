from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import JSONResponse
from starlette.responses import PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from datetime import datetime
import asyncio
import json
import csv
import io
from ..database import database
from ..crud.template import send_template_to_whatsapp

router = APIRouter()

class GenerateMessageRequest(BaseModel):
    prompt: str

@router.post("/generate-message")
async def generate_message(request: GenerateMessageRequest):
    """
    Generates a WhatsApp message template based on a user prompt.
    """
    try:
        # Instead of using OpenAI, let's use a simple rule-based system
        prompt_lower = request.prompt.lower()
        message = None

        if "diwali" in prompt_lower:
            message = "Hello {name}, Diwali greetings! Wishing you joy, prosperity, and success this festive season. Namaste!"
        elif "new year" in prompt_lower:
            message = "Hello {name}, Happy New Year! Wishing you a wonderful year ahead filled with happiness and success."
        elif "birthday" in prompt_lower:
            message = "Hello {name}, Happy Birthday! Wishing you a fantastic day and a year full of joy."
        else:
            # Default template
            message = f"Hello {{name}}, {request.prompt.strip().capitalize()}"

        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))