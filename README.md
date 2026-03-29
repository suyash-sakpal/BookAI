# 📚 BookAI — Intelligent Document Analysis with NLP

> Upload a PDF or TXT file and let AI summarize it or answer your questions — powered by state-of-the-art NLP models.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 📄 **PDF & TXT Upload** | Upload documents in `.pdf` or `.txt` format |
| 🧠 **Extractive Summary (spaCy)** | Fast rule-based extractive summarization using spaCy |
| 🤖 **Abstractive Summary (BART)** | Deep abstractive summarization using Facebook's BART-large-CNN model |
| 🔗 **Graph-based Summary (LexRank)** | Graph-based extractive summarization using LexRank |
| ❓ **Question & Answer (BERT)** | Ask any question about your document; answered by BERT fine-tuned on SQuAD |
| 🖥️ **Desktop GUI (Tkinter)** | A clean, dark-themed desktop application built with Tkinter |
| 🌐 **Web Interface (Flask)** | A REST API + web frontend powered by Flask |

---

## 🏗️ Project Structure

```
BookAI/
├── main.py            # Tkinter desktop application entry point
├── web_app.py         # Flask web application & REST API
├── summarizers.py     # Summarization logic (spaCy, BART, LexRank)
├── qa_model.py        # Question-Answering using BERT
├── utils.py           # PDF text extraction & file upload helpers
├── index.html         # Frontend HTML for the web interface
└── requirements.txt   # Python dependencies
```

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/suyash-sakpal/BookAI.git
cd BookAI
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the spaCy language model

```bash
python -m spacy download en_core_web_sm
```

> **Note:** The first run will automatically download the BART and BERT model weights from Hugging Face (~1.5 GB total). Ensure you have a stable internet connection.

---

## ▶️ Usage

### Desktop Application (Tkinter)

```bash
python main.py
```

- Click **Upload Document** to load a `.pdf` or `.txt` file.
- Switch to the **Summarize** tab and choose your summarization method.
- Switch to the **Q & A** tab, type your question, and click **Get Answer**.

---

### Web Application (Flask)

```bash
python web_app.py
```

Open your browser and navigate to: **[http://localhost:5000](http://localhost:5000)**

#### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serve the web frontend |
| `POST` | `/api/upload` | Upload a PDF or TXT file |
| `POST` | `/api/summarize` | Summarize the uploaded document |
| `POST` | `/api/qa` | Ask a question about the uploaded document |

**`POST /api/summarize`** — Request body:
```json
{ "method": "spacy" }   // Options: "spacy", "bart", "lexrank"
```

**`POST /api/qa`** — Request body:
```json
{ "question": "What is the main topic of the document?" }
```

---

## 🧩 Models Used

| Model | Source | Purpose |
|---|---|---|
| `en_core_web_sm` | spaCy | Tokenization & sentence segmentation |
| `facebook/bart-large-cnn` | Hugging Face | Abstractive summarization |
| `bert-large-uncased-whole-word-masking-finetuned-squad` | Hugging Face | Question Answering |
| LexRank | `lexrank` package | Graph-based extractive summarization |

---

## 📦 Dependencies

```
PyMuPDF       # PDF text extraction
spacy         # NLP & extractive summarization
torch         # PyTorch backend for transformers
transformers  # BART & BERT models from Hugging Face
lexrank       # LexRank graph-based summarization
SpeechRecognition
Flask         # Web framework for the REST API
```

---

## 🖼️ Screenshots

### Desktop Application
The desktop GUI features a dark, professional theme with tabbed navigation for **Summarize** and **Q & A** modes.

### Web Interface
The web server exposes a clean REST API and serves the frontend at `http://localhost:5000`.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Suyash Sakpal**
- GitHub: [@suyash-sakpal](https://github.com/suyash-sakpal)
- Email: suyashsakpal46@gmail.com

---

<p align="center">Made with ❤️ using Python, Hugging Face Transformers & spaCy</p>