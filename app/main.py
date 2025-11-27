from pathlib import Path
from fastapi import FastAPI, Request

app = FastAPI(title="Sanitize API")

# Load banned words from: app/banned_words.txt
BANNED_WORDS = []
BANNED_PATH = Path(__file__).resolve().parent / "banned_words.txt"

if BANNED_PATH.exists():
    content = BANNED_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    for line in lines:
        BANNED_WORDS.append(line)

def sanitize(text, banned_words):
    lower_text = text.lower()

    for w in banned_words:
        if w == "":
            continue  # prevent infinite loop if an empty line exists

        target = w.lower()
        idx = lower_text.find(target)

        while idx != -1:
            original = text[idx: idx + len(w)]

            if len(original) <= 2:
                masked = "*" * len(original)
            else:
                masked = original[0] + ("*" * (len(original) - 2)) + original[-1]

            text = text[:idx] + masked + text[idx + len(w):]
            lower_text = text.lower()
            idx = lower_text.find(target, idx + len(masked))

    return text

@app.post("/sanitize")
async def sanitize_endpoint(request: Request):
    data = await request.json()
    text = data.get("text", "")
    cleaned = sanitize(text, BANNED_WORDS)
    return {"cleaned": cleaned}
