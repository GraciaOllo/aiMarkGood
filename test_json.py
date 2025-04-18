import json

with open("app/correct_answers.json") as f:
    correct_answers = json.load(f)

print(correct_answers)
