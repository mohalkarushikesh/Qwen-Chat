import os
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent.parent

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    info = {"flask": "ok", "ollama": None, "model": MODEL}
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        info["ollama"] = "ok"
        info["available_models"] = models
        info["model_found"] = any(MODEL in m for m in models)
    except Exception as e:
        info["ollama"] = f"error: {str(e)}"
    return jsonify(info)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400

    print(f"[chat] prompt={prompt[:80]!r}")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        print(f"[chat] ollama status={response.status_code}")
        response.raise_for_status()

    except requests.exceptions.ConnectionError as e:
        print(f"[chat] connection error: {e}")
        return jsonify({"error": "Cannot connect to Ollama. Is it running?"}), 503

    except requests.exceptions.Timeout:
        return jsonify({"error": "Ollama timed out after 120s."}), 504

    except requests.exceptions.HTTPError as e:
        body = ""
        try:
            body = response.text
        except Exception:
            pass
        print(f"[chat] http error: {e} | body: {body}")
        return jsonify({"error": f"Ollama HTTP error: {e}", "detail": body}), 500

    except Exception as e:
        print(f"[chat] unexpected error: {e}")
        return jsonify({"error": str(e)}), 500

    try:
        result = response.json()
    except Exception as e:
        print(f"[chat] json parse error: {e} | raw: {response.text[:300]}")
        return jsonify({"error": "Failed to parse Ollama response", "raw": response.text[:300]}), 500

    resp_text = result.get("response", "")
    if not resp_text:
        print(f"[chat] empty response. full result keys: {list(result.keys())}")
        return jsonify({"error": "Ollama returned empty response", "debug": str(result)[:300]}), 500

    return jsonify({"response": resp_text})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    print(f"\n  Flask ready — http://localhost:{port}")
    print(f"  Check Ollama:  http://localhost:{port}/health\n")
    app.run(host="0.0.0.0", port=port, debug=False)