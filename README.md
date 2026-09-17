# SAARTHI.AI — Full Project

Ancient Wisdom. Modern Intelligence.

## Project structure

- `frontend/` — Next.js + TypeScript + Tailwind CSS frontend
- `backend/` — FastAPI + FAISS + Sentence Transformers + OpenAI RAG backend

## 1. Start frontend

Open PowerShell in the `frontend` folder:

```powershell
cd frontend
npm install
npm run dev
```

Open: http://localhost:3000

## 2. Start backend

Open a second PowerShell window in the `backend` folder:

```powershell
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your real OpenAI API key to `backend/.env`:

```env
OPENAI_API_KEY=sk-...
```

Then start:

```powershell
python -m uvicorn main:app --reload
```

Backend: http://127.0.0.1:8000

Never share or commit your API key.
