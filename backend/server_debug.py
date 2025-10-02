from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os

app = FastAPI()

# Get current directory and setup paths
BASE_DIR = Path(__file__).parent.absolute()
STATIC_DIR = BASE_DIR / "static"

@app.get("/debug")
async def debug_info():
    # Collect debug information
    info = {
        "base_dir": str(BASE_DIR),
        "static_dir": str(STATIC_DIR),
        "static_exists": STATIC_DIR.exists(),
        "static_is_dir": STATIC_DIR.is_dir() if STATIC_DIR.exists() else False,
        "static_contents": [],
        "current_working_dir": str(Path.cwd()),
        "index_html_exists": (STATIC_DIR / "index.html").exists() if STATIC_DIR.exists() else False
    }
    
    # List files in static directory if it exists
    if STATIC_DIR.exists() and STATIC_DIR.is_dir():
        info["static_contents"] = [str(f.relative_to(STATIC_DIR)) for f in STATIC_DIR.glob("**/*")]
    
    return JSONResponse(content=info)

@app.get("/")
async def root():
    return {"message": "Server is running", "debug_url": "/debug"}

# Mount static files
if STATIC_DIR.exists() and STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/direct-file")
async def get_file_directly():
    file_path = STATIC_DIR / "index.html"
    if file_path.exists():
        return FileResponse(file_path)
    return {"error": "File not found", "path": str(file_path)}