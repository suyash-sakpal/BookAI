import fitz

uploaded_text = ""  # Shared across modules

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def upload_file(result_box):
    global uploaded_text
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf;*.PDF"), ("Text Files", "*.txt;*.TXT")])
    if not file_path:
        return
    lower = file_path.lower()
    if lower.endswith(".pdf"):
        uploaded_text = extract_text_from_pdf(file_path)
    elif lower.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            uploaded_text = f.read()
    else:
        uploaded_text = ""
        result_box.insert("end", "Unsupported file type. Please choose PDF or TXT.\n")
        return
    # Normalize whitespace and lightly trim extremely large docs for UI
    if uploaded_text:
        uploaded_text = uploaded_text.replace("\r\n", "\n").replace("\r", "\n")
    result_box.insert("end", "File uploaded and text extracted!\n")
