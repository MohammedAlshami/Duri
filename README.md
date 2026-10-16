# Duri 🎭

Duri is a small, fun interactive **companion bot** with a personality: it is witty,
playful, supportive and teasing, and answers as a friendly cartoon character.
Each reply is JSON-structured so the frontend can swap the character's **emotion**
and the **scene background** on the fly — the character visually reacts to the
conversation.

Built with Python, Django, and the OpenAI API. Originally created around a
university/club demo (see the `bg/` and `characters/` assets).

---

## Features

- 💬 Chat interface that streams responses through a Django endpoint
- 🎨 Character reactions: per-response `emotion` picks one of several SVG faces
- 🌄 Dynamic scenes: `background_image` chooses one of several locations
- 🌐 Multilingual small talk: Russian, German, Arabic and Japanese
- 🗣️ Voice capture in the browser (`audio.html`) via the Web MediaRecorder API
- 🔥 Optional Firebase Realtime Database chat history per user

## Demo flow

1. The user picks a character (from `characterSelection.html`).
2. The user sends a message → Django view builds the prompt and calls OpenAI.
3. The reply is JSON like:

   ```json
   { "response": "i'm listening!", "background_image": "...", "emotion": "..." }
   ```

4. The frontend swaps the character + background to match.

## Project layout

```
Duri/
├── Duri/              # Django project (settings, urls, wsgi, asgi)
├── backend/           # app: views, templates (characterSelection, chat, story, index)
│   └── templates/     # HTML pages
├── audio.html         # Standalone audio recorder demo
├── main.html          # Marketing-ish landing page
├── requirements.txt   # Python dependencies
└── db.sqlite3         # (local dev database — not committed in clean builds)
```

## Requirements

- Python 3.10+ (tested on 3.11)
- `pip` and (recommended) a virtual environment
- An OpenAI API key
- Optional: Firebase Realtime Database credentials if you want chat history

## Setup

```bash
# 1. Clone
git clone https://github.com/MohammedAlshami/Duri.git
cd Duri

# 2. Create + activate venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure secrets (never commit these)
cp .env.example .env   # if present; or set env vars directly
export OPENAI_API_KEY=sk-...               # macOS/Linux
# setx OPENAI_API_KEY sk-...                # Windows PowerShell

# Optional (Firebase chat history):
export FIREBASE_API_KEY=...
export FIREBASE_AUTH_DOMAIN=...
export FIREBASE_DB_URL=...
export FIREBASE_PROJECT_ID=...
export FIREBASE_STORAGE_BUCKET=...
export FIREBASE_MESSAGING_SENDER_ID=...
export FIREBASE_APP_ID=...

# 5. Django setup
python manage.py migrate   # note: manage.py isn't in this repo yet; use `django-admin` or run via runserver below
# The repo ships settings under Duri/. If you add a manage.py, even better.

# 6. Collect static (optional)
python manage.py collectstatic --noinput

# 7. Run
python manage.py runserver 0.0.0.0:8000
# Then open http://127.0.0.1:8000/
```

> **No `manage.py`?** This repo was scaffolded without one. You can run Django via:
>
> `django-admin runserver --settings=Duri.settings`
>
> or add a `manage.py` at the repo root.

## Environment variables

| Variable | Required | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | yes | OpenAI chat completions (gpt-3.5-turbo) |
| `DJANGO_SECRET_KEY` | recommended | Replaces the insecure default for production |
| `FIREBASE_API_KEY`, `FIREBASE_AUTH_DOMAIN`, `FIREBASE_DB_URL`, `FIREBASE_PROJECT_ID`, `FIREBASE_STORAGE_BUCKET`, `FIREBASE_MESSAGING_SENDER_ID`, `FIREBASE_APP_ID` | optional | Enables persisted chat history |

## License & credits

Personal project — no explicit license attached. Assets (SVGs, backdrops) are
hosted on a CDN and referenced from templates.

Thanks for reading.
