from flask import Flask, request, jsonify
from flask_cors import CORS
import os

key = os.environ.get("OPENAI_API_KEY")


app = Flask(__name__)
CORS(app)


@app.get("/")
def health():
    # Simple health check so you know the server is running
    return "OK"


@app.post("/decide")
def decide():
    """Accepts JSON and returns a poker decision.

    Expected JSON (example):
      {"player": {...}, "ctx": {...}, "baseDecision": {...}}

    For now, this returns a stub response. We'll replace the TODO section with
    an OpenAI call later.
    """
    payload = request.get_json(silent=True) or {}

    player = payload.get("player", {})
    ctx = payload.get("ctx", {})
    base_decision = payload.get("baseDecision")

    # TODO: Call OpenAI here using your API key from an environment variable.
    #   - Build a prompt from (player, ctx, base_decision)
    #   - Send it to the OpenAI API
    #   - Parse/validate the JSON decision returned

    # Minimal stub decision (safe default)
    return jsonify({
        "action": "fold",
        "amount": None,
        "debug": {
            "playerName": player.get("name"),
            "street": ctx.get("phase") or ctx.get("street"),
            "usedBaseDecision": base_decision is not None,
        },
    })


if __name__ == "__main__":
    # Change port if you like; 5055 keeps it separate from common dev servers
    app.run(host="127.0.0.1", port=5055, debug=True)