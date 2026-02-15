from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

def prune_empty(obj):
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            pv = prune_empty(v)
            if pv in ({}, [], None):
                continue
            cleaned[k] = pv
        return cleaned
    elif isinstance(obj, list):
        cleaned = [prune_empty(v) for v in obj]
        return [v for v in cleaned if v not in ({}, [], None)]
    else:
        return obj

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
    raw_player = payload.get("player", {})
    raw_ctx = payload.get("ctx", {})
    base_decision = payload.get("baseDecision")

    player = prune_empty(raw_player)
    ctx = prune_empty(raw_ctx)

    print("\n================ BOT DECISION REQUEST ================")

    player_name = player.get("name")
    print(f"Player: {player_name}")

    print("\n--- Hole Cards (from LLM.js) ---")
    print(json.dumps(player.get("holeCards"), indent=2))

    print("\n--- Community Cards (from LLM.js) ---")
    print(json.dumps(ctx.get("communityCards"), indent=2))

    print("\n--- Base Decision ---")
    print(json.dumps(base_decision, indent=2))

    print("\n--- Street / Phase ---")
    print(ctx.get("phase") or ctx.get("street"))

    print("\n--- Recent History ---")
    print(json.dumps(ctx.get("recentHistory"), indent=2))

    print("\n--- History By Street ---")
    print(json.dumps(ctx.get("historyByStreet"), indent=2))

    print("\n--- Player Snapshot (Full) ---")
    print(json.dumps(player, indent=2))

    print("======================================================\n", flush=True)

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
