from flask import Flask, request, jsonify

app = Flask(__name__)

# Mapping huruf ke angka
REPLACE_MAP = {
    "a": "4",
    "s": "5",
    "i": "1",
    "e": "3",
    "o": "0"
}

def replace_text_func(text):
    result = ""

    for char in text:
        low = char.lower()
        if low in REPLACE_MAP:
            result += REPLACE_MAP[low]
        else:
            result += char

    return result


@app.post("/replace")
def replace_endpoint():
    data = request.get_json(silent=True) or {}

    if "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"]
    replaced = replace_text_func(text)

    return jsonify({"result": replaced})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
