def score_answers(correct, user, correct_pts, wrong_pts, blank_pts):
    score = 0
    details = []
    for i, correct_ans in enumerate(correct):
        try:
            user_ans = user[i]
        except IndexError:
            user_ans = None

        if not user_ans:
            score += blank_pts
            details.append({
                "q": i + 1,
                "status": "blank",
                "answer": None,
                "correct": correct_ans
            })
        elif user_ans == correct_ans:
            score += correct_pts
            details.append({
                "q": i + 1,
                "status": "correct",
                "answer": user_ans,
                "correct": correct_ans
            })
        else:
            score += wrong_pts
            details.append({
                "q": i + 1,
                "status": "wrong",
                "answer": user_ans,
                "correct": correct_ans
            })

    return {
        "score": score,
        "details": details
    }
