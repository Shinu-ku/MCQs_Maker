from flask import Blueprint, render_template, request, jsonify
import os, json
from .utils import load_chapters, load_questions

main = Blueprint("main", __name__)

@main.route("/")
def home():
    chapters = load_chapters()
    return render_template("index.html", chapters=chapters)

@main.route("/quiz/<chapter>")
def quiz(chapter):
    data = load_questions(chapter)
    return render_template("quiz.html", chapter=chapter, questions=data["questions"])

@main.route("/check-answer", methods=["POST"])
def check_answer():
    data = request.json
    chapter = data["chapter"]
    q_index = data["q_index"]
    user_answer = data["answer"]

    questions = load_questions(chapter)["questions"]
    correct = questions[q_index]["answer"]
    explanation = questions[q_index]["explanation"]

    return jsonify({
        "correct": correct,
        "is_correct": (user_answer == correct),
        "explanation": explanation
    })
