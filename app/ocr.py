import pytesseract
from PIL import Image

def extract_answers_from_image(img_path: str):
    image = Image.open(img_path)
    raw_text = pytesseract.image_to_string(image)
    
    # Simple normalization (You can improve with regex)
    lines = [line.strip().upper() for line in raw_text.splitlines() if line.strip()]
    answers = [line[-1] for line in lines if line[-1] in {"A", "B", "C", "D"}]
    
    return answers

def grade_answers(user, correct, scheme):
    score = 0
    for u, c in zip(user, correct):
        if u == c:
            score += scheme.get("correct", 1)
        else:
            score += scheme.get("wrong", 0)
    return {"score": score}

