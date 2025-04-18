import os
import uuid
import json
import shutil
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.pdf_generator import generate_result_pdf
from app.ocr import extract_answers_from_image
from app.scorer import score_answers

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")


STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

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
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}_{file.filename}")
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

    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": result_data["score"],
        "details": result_data["details"],
        "ocr_answers": extracted_answers,
        "student": name,
        "subject": subject,
        "pdf_path": pdf_path
    })

@app.get("/download_pdf")
async def download_pdf(path: str):
    if os.path.exists(path):
        return FileResponse(path, media_type='application/pdf', filename=os.path.basename(path))
    return {"error": "PDF not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
