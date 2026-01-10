import tkinter as tk
from tkinter import ttk, Text, Scrollbar, END, messagebox, filedialog, Label

from summarizers import summarize_with_spacy, summarize_with_bart, lexrank_summary
from qa_model import get_answer
from utils import upload_file

# Initialize Tkinter
root = tk.Tk()
root.title("BookAI - NLP Application")
root.geometry("1000x720")
root.minsize(900, 640)
root.configure(bg="#0b1221")

# -----------------
# Theming and Styles
# -----------------
style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass

primary_bg = "#0b1221"
surface_bg = "#121a2b"
panel_bg = "#0e1627"
accent = "#EC8305"
accent_hover = "#ff9d2a"
text_primary = "#e6eaf2"
text_muted = "#9aa6bf"

style.configure("TFrame", background=primary_bg)
style.configure("Surface.TFrame", background=surface_bg)
style.configure("Panel.TFrame", background=panel_bg)
style.configure("Title.TLabel", font=("Helvetica", 20, "bold"), foreground=text_primary, background=primary_bg)
style.configure("SubTitle.TLabel", font=("Helvetica", 12), foreground=text_muted, background=primary_bg)
style.configure("Section.TLabel", font=("Helvetica", 12, "bold"), foreground=text_primary, background=surface_bg)
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("Accent.TButton", foreground="#0b1221", background=accent)
style.map("Accent.TButton", background=[("active", accent_hover), ("!active", accent)])

# -------------
# Layout Frames
# -------------
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

header = ttk.Frame(root, style="TFrame")
header.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))

title = ttk.Label(header, text="BookAI", style="Title.TLabel")
subtitle = ttk.Label(header, text="Summarize documents and ask questions with AI", style="SubTitle.TLabel")
title.grid(row=0, column=0, sticky="w")
subtitle.grid(row=1, column=0, sticky="w")

toolbar = ttk.Frame(root, style="Surface.TFrame")
toolbar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
toolbar.columnconfigure(0, weight=1)

upload_button = ttk.Button(toolbar, text="Upload Document (.pdf / .txt)", command=lambda: upload_file(result_box), style="Accent.TButton")
upload_button.grid(row=0, column=0, sticky="w", pady=12, padx=12)

content = ttk.Frame(root, style="TFrame")
content.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
content.columnconfigure(0, weight=1)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=0)

# Tabs for features
notebook = ttk.Notebook(content)
notebook.grid(row=0, column=0, sticky="nsew")

# ----------------------
# Summarization Tab
# ----------------------
tab_summ = ttk.Frame(notebook, style="Surface.TFrame")
tab_summ.columnconfigure(0, weight=1)
tab_summ.rowconfigure(1, weight=1)
notebook.add(tab_summ, text="Summarize")

summ_controls = ttk.Frame(tab_summ, style="Surface.TFrame")
summ_controls.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

summ_label = ttk.Label(summ_controls, text="Choose a summarization method", style="Section.TLabel")
summ_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

spacy_button = ttk.Button(summ_controls, text="Summarize with spaCy", command=lambda: summarize_with_spacy(result_box))
spacy_button.grid(row=1, column=0, sticky="w", padx=(0, 8))

bart_button = ttk.Button(summ_controls, text="Summarize with BART", command=lambda: summarize_with_bart(result_box))
bart_button.grid(row=1, column=1, sticky="w", padx=(0, 8))

lexrank_button = ttk.Button(summ_controls, text="Summarize with LexRank", command=lambda: lexrank_summary(result_box))
lexrank_button.grid(row=1, column=2, sticky="w")

# ----------------------
# Q&A Tab
# ----------------------
tab_qa = ttk.Frame(notebook, style="Surface.TFrame")
tab_qa.columnconfigure(0, weight=1)
notebook.add(tab_qa, text="Q & A")

qa_controls = ttk.Frame(tab_qa, style="Surface.TFrame")
qa_controls.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
qa_controls.columnconfigure(0, weight=1)

qa_label = ttk.Label(qa_controls, text="Ask a question about the uploaded content", style="Section.TLabel")
qa_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

question_entry = Text(qa_controls, height=3, width=50, font=("Helvetica", 12), wrap="word", relief="solid", borderwidth=1, bg="#1b2436", fg=text_primary, insertbackground=text_primary)
question_entry.grid(row=1, column=0, columnspan=3, sticky="ew")

answer_button = ttk.Button(qa_controls, text="Get Answer", command=lambda: get_answer(question_entry, result_box), style="Accent.TButton")
answer_button.grid(row=2, column=0, sticky="w", pady=10)


# ----------------------
# Results Pane (shared)
# ----------------------
results_frame = ttk.Frame(content, style="Panel.TFrame")
results_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
results_frame.columnconfigure(0, weight=1)
results_frame.rowconfigure(1, weight=1)

results_label = ttk.Label(results_frame, text="Results", style="Section.TLabel")
results_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 0))

result_container = ttk.Frame(results_frame, style="Panel.TFrame")
result_container.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
result_container.columnconfigure(0, weight=1)
result_container.rowconfigure(0, weight=1)

result_box = Text(result_container, height=12, width=80, font=("Helvetica", 12), wrap="word", relief="flat", borderwidth=0, bg="#0f1a2f", fg=text_primary, insertbackground=text_primary)
result_box.grid(row=0, column=0, sticky="nsew")

scroll = Scrollbar(result_container, command=result_box.yview)
scroll.grid(row=0, column=1, sticky="ns")
result_box.config(yscrollcommand=scroll.set)

# Run App
root.mainloop()
