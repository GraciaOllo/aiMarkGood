from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import uuid

def generate_result_pdf(data: dict) -> str:
    os.makedirs("temp", exist_ok=True)
    pdf_path = f"temp/{uuid.uuid4()}_result.pdf"

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, f"MCQ Exam Result Sheet")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 90, f"Student Name: {data['student']}")
    c.drawString(100, height - 110, f"Subject: {data['subject']}")
    c.drawString(100, height - 130, f"Score: {data['score']} / {data['total_questions']}")

    c.drawString(100, height - 160, "Answer Breakdown:")
    y = height - 180
    for item in data["details"]:
        line = f"Q{item['q']}: {item['status']}"
        if item["status"] == "wrong":
            line += f" (You: {item['answer']} | Correct: {item['correct']})"
        c.drawString(120, y, line)
        y -= 20

    c.save()
    return pdf_path
