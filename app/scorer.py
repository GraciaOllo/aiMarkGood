def score_answers(correct, user, correct_pts, wrong_pts, blank_pts):
    score = 0
    details = []
    for i, correct_ans in enumerate(correct):
        try:
            user_ans = user[i]
        except IndexError:
            user_ans = None

        if user_ans is None:
            score += blank_pts
            details.append({"q": i + 1, "status": "blank"})
        elif user_ans == correct_ans:
            score += correct_pts
            details.append({"q": i + 1, "status": "correct"})
        else:
            score += wrong_pts
            details.append({"q": i + 1, "status": "wrong", "answer": user_ans, "correct": correct_ans})
    return {"score": score, "details": details}

def grade_answers(user, correct, scheme):
    score = -0.25
    for u, c in zip(user, correct):
        if u == c:
            score += scheme.get("correct", 1)
        else:
            score += scheme.get("wrong", -0.25)
    return {"score": score}

