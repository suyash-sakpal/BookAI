import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from tkinter import END, messagebox
import utils

# Load BERT
bert_tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
bert_model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def get_answer(question_entry, result_box):
    question = question_entry.get("1.0", END).strip()
    if not utils.uploaded_text or not question:
        messagebox.showerror("Error", "Please upload a text file and ask a question.")
        return

    # Truncate long contexts and prefer truncating only the context (second sequence)
    try:
        inputs = bert_tokenizer.encode_plus(
            question,
            utils.uploaded_text,
            return_tensors='pt',
            max_length=512,
            truncation='only_second'
        )
        input_ids, attention_mask = inputs['input_ids'], inputs['attention_mask']

        with torch.no_grad():
            outputs = bert_model(input_ids, attention_mask=attention_mask)
            start_logits, end_logits = outputs.start_logits, outputs.end_logits

        start_index = torch.argmax(start_logits)
        end_index = torch.argmax(end_logits) + 1

        if start_index >= end_index:
            answer = "I'm sorry, I couldn't find an answer."
        else:
            answer = bert_tokenizer.convert_tokens_to_string(
                bert_tokenizer.convert_ids_to_tokens(input_ids[0][start_index:end_index])
            )

        result_box.insert(END, f"Q: {question}\nA: {answer.strip()}\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Question answering failed: {e}")
