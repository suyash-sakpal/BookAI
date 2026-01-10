import spacy
from transformers import BartTokenizer, BartForConditionalGeneration
from lexrank import LexRank
from tkinter import END, messagebox

import utils

# Load models
spacy_nlp = spacy.load("en_core_web_sm")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

def summarize_with_spacy(result_box):
    if not utils.uploaded_text:
        messagebox.showerror("Error", "Please upload a document (PDF/TXT) first.")
        return
    # Use a capped slice to keep performance reasonable
    text = utils.uploaded_text[:8000]
    doc = spacy_nlp(text)
    sentences = list(doc.sents)
    if not sentences:
        messagebox.showerror("Error", "No sentences found to summarize.")
        return
    scores = {i: len(sent.text) for i, sent in enumerate(sentences)}
    ranked = sorted(scores, key=scores.get, reverse=True)
    top = min(3, len(sentences))
    summary = ' '.join([sentences[i].text for i in ranked[:top]])
    if not summary.strip():
        messagebox.showerror("Error", "Failed to generate summary.")
        return
    result_box.insert(END, "Extractive Summary (spaCy):\n" + summary + "\n\n")

def summarize_with_bart(result_box):
    if not utils.uploaded_text:
        messagebox.showerror("Error", "Please upload a document (PDF/TXT) first.")
        return
    try:
        inputs = bart_tokenizer(utils.uploaded_text, max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = bart_model.generate(inputs["input_ids"], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        if not summary.strip():
            messagebox.showerror("Error", "Failed to generate abstractive summary.")
            return
        result_box.insert(END, "Abstractive Summary (BART):\n" + summary + "\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error generating abstractive summary: {e}")

def lexrank_summary(result_box):
    if not utils.uploaded_text:
        messagebox.showerror("Error", "Please upload a document (PDF/TXT) first.")
        return
    try:
        # Keep computation bounded
        text = utils.uploaded_text[:8000]
        sentences = [s for s in text.split('\n') if s.strip()]
        if not sentences:
            messagebox.showerror("Error", "No sentences found to summarize.")
            return
        lexrank = LexRank(sentences)
        size = min(3, len(sentences))
        summary = lexrank.get_summary(sentences, summary_size=size)
        joined = ' '.join(summary).strip()
        if not joined:
            messagebox.showerror("Error", "Failed to generate LexRank summary.")
            return
        result_box.insert(END, "Extractive Summary (LexRank):\n" + joined + "\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"LexRank error: {e}")
