# AI MCQ Marker Web App
i had a small issue with some git accounts birelles acount wwas clashing thats why you are seeing 2 contibutors i am the only contributor i resolved the conflict


This is a web application that uses AI-powered Optical Character Recognition (OCR) to automatically grade multiple-choice (MCQ) answer sheets uploaded as images. The app is built using **FastAPI**, **Jinja2**, and **Pytesseract**.

## 🚀 Features

- Upload scanned answer sheet images (e.g. from mobile phone camera).
- AI-based answer extraction using OCR (via Tesseract).
- Customizable marking scheme:
  - Define points for correct, wrong, and blank answers.
- Generates a score and detailed feedback for each question.
- Automatically generates a **PDF report** with student name, subject, score, and answer breakdown.
- User-friendly interface built with HTML + CSS.
- Downloadable PDF result sheet.

## 🧠 Tech Stack

- **Python 3.x**
- **FastAPI** (backend)
- **Jinja2** (HTML templating)
- **Pytesseract** + **PIL** (OCR)
- **ReportLab** (PDF generation)
- **HTML/CSS** (frontend)

## 📦 Requirements

- Python 3.7+
- Tesseract OCR installed  
  👉 [Download Tesseract](https://github.com/tesseract-ocr/tesseract)

Install dependencies:

```bash
pip install -r requirements.txt
🛠️ How to Run
Ensure Python and Tesseract are installed on your system.

Place your correct answers in correct_answers.json (as a JSON list).

From the project root, start the FastAPI server:
📄 How to Use
Fill in the student name and subject.

Upload a clear image of the student's answer sheet.

Enter your marking scheme:

Points for correct answers

Penalty for wrong answers

Points for blanks (can be zero)
