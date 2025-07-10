# Lexi.sg RAG Backend Test

> A FastAPI-based Retrieval-Augmented Generation (RAG) backend for legal query answering

&#x20;

---

## 📦 Prerequisites

- Python 3.10 or higher
- [UV](https://github.com/astral-sh/uv) installed globally

  ```bash
  pip install uv
  ```

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/santanu2310/lexi.sg-rag-backend-test.git
cd lexi.sg-rag-backend-test
```

### 2. Create Virtual Environment & Install Dependencies

```bash
uv venv .venv
uv pip sync
```

### 3. Activate the Virtual Environment

#### 🐧 Linux/macOS

```bash
source .venv/bin/activate
```

#### 🪟 Windows

```bash
.\.venv\Scripts\activate
```

---

## 📚 Embed Documents

This step will:

- ▼ Optionally delete the existing embeddings
- ▼ Load and embed documents from the `data/` folder
- ▼ Store them in the vector store

```bash
python3 -m app.embed_docs --delete_old_embedding
```

---

## 🏃 Run the Application

Start the FastAPI server in development mode:

```bash
uvicorn app.main:app --reload
```

Navigate to the interactive API docs at:

➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

---


_Happy coding!_