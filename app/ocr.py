import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_answers_from_image(img_path: str):
    image = Image.open(img_path).convert("L")
    raw_text = pytesseract.image_to_string(image)
    lines = [line.strip().upper() for line in raw_text.splitlines() if line.strip()]
    answers = [line[-1] for line in lines if line[-1] in {"A", "B", "C", "D"}]
    return answers
