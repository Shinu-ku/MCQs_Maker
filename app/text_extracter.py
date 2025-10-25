# app/text_extracter.py

import os
import json
import re
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def extract_mcqs(text):
    """
    Extract structured MCQs from text using regex.
    Handles variations like 'View Answer', inconsistent line breaks, etc.
    """
    # Normalize text
    text = re.sub(r'\r', '', text)  # remove carriage returns
    text = re.sub(r'View Answer', '', text, flags=re.IGNORECASE)  # remove "View Answer"
    text = re.sub(r'\n+', '\n', text)  # collapse multiple blank lines

    # Updated pattern
    pattern = re.compile(
        r"(?P<question>\d+\..*?)\n"  # Question start
        r"a\)\s*(?P<a>.*?)\n"
        r"b\)\s*(?P<b>.*?)\n"
        r"c\)\s*(?P<c>.*?)\n"
        r"d\)\s*(?P<d>.*?)\n"
        r"(?:.*?Answer:\s*(?P<answer>[a-dA-D]).*?)?"  # answer can appear after other text
        r"(?:Explanation:\s*(?P<explanation>.*?))?"   # explanation is optional
        r"(?=\n\d+\.|$)",  # lookahead for next question or EOF
        re.DOTALL
    )

    mcqs = []
    for match in pattern.finditer(text):
        question = match.group("question").strip()
        options = [
            match.group("a").strip(),
            match.group("b").strip(),
            match.group("c").strip(),
            match.group("d").strip(),
        ]
        answer = (match.group("answer") or "").strip()
        explanation = (match.group("explanation") or "").strip()

        mcqs.append({
            "question": question,
            "options": options,
            "answer": answer,
            "explanation": explanation,
        })

    return mcqs


def process_pdfs():
    """Read all PDFs from /app/PDFs and generate structured MCQ JSON files."""
    pdf_folder = os.path.join(os.path.dirname(__file__), "PDFs")
    output_folder = os.path.join(os.path.dirname(__file__), "..", "mcqs")
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(pdf_folder):
        if not file.endswith(".pdf"):
            continue

        print(f"📄 Processing: {file}")
        pdf_path = os.path.join(pdf_folder, file)

        text = extract_text_from_pdf(pdf_path)
        mcqs = extract_mcqs(text)

        output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"chapter": file, "questions": mcqs}, f, indent=4, ensure_ascii=False)

        print(f"✅ Saved {len(mcqs)} MCQs → {output_path}")


if __name__ == "__main__":
    process_pdfs()
