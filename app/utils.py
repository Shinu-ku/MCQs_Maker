import os, json

MCQ_DIR = "mcqs"

def load_chapters():
    return [f.replace(".json", "") for f in os.listdir(MCQ_DIR) if f.endswith(".json")]

def load_questions(chapter):
    with open(f"{MCQ_DIR}/{chapter}.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(chapter, data):
    with open(f"{MCQ_DIR}/{chapter}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
