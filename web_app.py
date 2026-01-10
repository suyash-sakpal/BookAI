import os
from typing import Dict

from flask import Flask, render_template, request, jsonify

import torch
import spacy
from transformers import (
    BertTokenizer,
    BertForQuestionAnswering,
    BartTokenizer,
    BartForConditionalGeneration,
)
from lexrank import LexRank

from utils import extract_text_from_pdf


app = Flask(__name__, static_folder="static", template_folder="templates")

# -------------------------
# Model Initialization
# -------------------------
spacy_nlp = spacy.load("en_core_web_sm")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

bert_tokenizer = BertTokenizer.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
)
bert_model = BertForQuestionAnswering.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
)


# Simple in-memory storage for uploaded text per sessionless demo
STATE: Dict[str, str] = {"uploaded_text": ""}


def get_uploaded_text() -> str:
    return STATE.get("uploaded_text", "")


def set_uploaded_text(text: str) -> None:
    STATE["uploaded_text"] = text or ""


# -------------------------
# Summarization helpers
# -------------------------
def summarize_spacy(text: str) -> str:
    if not text:
        return ""
    doc = spacy_nlp(text)
    sentences = list(doc.sents)
    if not sentences:
        return ""
    scores = {i: len(sent.text) for i, sent in enumerate(sentences)}
    ranked = sorted(scores, key=scores.get, reverse=True)
    summary = " ".join([sentences[i].text for i in ranked[:3]])
    return summary.strip()


def summarize_bart(text: str) -> str:
    if not text:
        return ""
    inputs = bart_tokenizer(
        text, max_length=1024, return_tensors="pt", truncation=True
    )
    summary_ids = bart_model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=50,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True,
    )
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()


def summarize_lexrank(text: str) -> str:
    if not text:
        return ""
    sentences = [s for s in text.split("\n") if s.strip()]
    if not sentences:
        return ""
    lexrank = LexRank(sentences)
    summary = lexrank.get_summary(sentences, summary_size=3)
    return " ".join(summary).strip()


def answer_question(question: str, context: str) -> str:
    if not question or not context:
        return ""
    inputs = bert_tokenizer.encode_plus(question, context, return_tensors="pt")
    input_ids, attention_mask = inputs["input_ids"], inputs["attention_mask"]
    with torch.no_grad():
        outputs = bert_model(input_ids, attention_mask=attention_mask)
        start_logits, end_logits = outputs.start_logits, outputs.end_logits
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1
    if start_index >= end_index:
        return ""
    answer = bert_tokenizer.convert_tokens_to_string(
        bert_tokenizer.convert_ids_to_tokens(input_ids[0][start_index:end_index])
    )
    return answer.strip()


# -------------------------
# Routes
# -------------------------
@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/upload")
def api_upload():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename.lower().endswith(".pdf"):
        # Save temp then extract with PyMuPDF
        temp_path = os.path.join(app.instance_path, "upload.pdf")
        os.makedirs(app.instance_path, exist_ok=True)
        file.save(temp_path)
        text = extract_text_from_pdf(temp_path)
        set_uploaded_text(text)
        return jsonify({"ok": True, "message": "PDF uploaded", "length": len(text)})
    elif file.filename.lower().endswith(".txt"):
        text = file.stream.read().decode("utf-8", errors="ignore")
        set_uploaded_text(text)
        return jsonify({"ok": True, "message": "Text uploaded", "length": len(text)})
    else:
        return jsonify({"ok": False, "error": "Unsupported file type"}), 400


@app.post("/api/summarize")
def api_summarize():
    body = request.get_json(silent=True) or {}
    method = (body.get("method") or "").lower()
    text = get_uploaded_text()
    if not text:
        return jsonify({"ok": False, "error": "No document uploaded"}), 400

    try:
        if method == "spacy":
            summary = summarize_spacy(text)
            kind = "Extractive (spaCy)"
        elif method == "bart":
            summary = summarize_bart(text)
            kind = "Abstractive (BART)"
        elif method == "lexrank":
            summary = summarize_lexrank(text)
            kind = "Extractive (LexRank)"
        else:
            return jsonify({"ok": False, "error": "Unknown method"}), 400
        return jsonify({"ok": True, "type": kind, "summary": summary})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/api/qa")
def api_qa():
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()
    context = get_uploaded_text()
    if not question:
        return jsonify({"ok": False, "error": "Question is required"}), 400
    if not context:
        return jsonify({"ok": False, "error": "No document uploaded"}), 400
    try:
        answer = answer_question(question, context)
        if not answer:
            answer = "I'm sorry, I couldn't find an answer."
        return jsonify({"ok": True, "answer": answer})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    # For local dev
    url = "http://localhost:5000"
    print("\n====================================")
    print(" BookAI web server starting…")
    print(f" Open in your browser: {url}")
    print("====================================\n")
    app.run(host="0.0.0.0", port=5000, debug=True)


