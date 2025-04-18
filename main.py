import os
import sys
import uuid
import json
import shutil
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Optional: only use if still running from /app directory
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Local imports
from app.pdf_generator import generate_result_pdf
from app.ocr import extract_answers_from_image
from app.scorer import score_answers

# Setup
BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Load answer key
with open(os.path.join(BASE_DIR, "correct_answers.json")) as f:
    correct_answers = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_image", response_class=HTMLResponse)
async def upload_image(
    request: Request,
    name: str = Form(...),
    subject: str = Form(...),
    correct_points: float = Form(...),
    wrong_points: float = Form(...),
    blank_points: float = Form(...),
    file: UploadFile = File(...)
):
    os.makedirs("temp", exist_ok=True)
    temp_path = f"temp/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_answers = extract_answers_from_image(temp_path)
    result = score_answers(correct_answers, extracted_answers, correct_points, wrong_points, blank_points)

    result_data = {
        "student": name,
        "subject": subject,
        "score": result["score"],
        "total_questions": len(correct_answers),
        "details": result["details"],
        "ocr_answers": extracted_answers
    }

    pdf_path = generate_result_pdf(result_data)

    return templates
