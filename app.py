import os
import base64
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not set")

client = genai.Client(api_key=api_key)

@app.route("/")
def home():
    return "Gemini Image Generator Running"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(force=True)

        if "prompt" not in data:
            return jsonify({"error": "Prompt missing"}), 400

        prompt = data["prompt"]

        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt],
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                return jsonify({"image": image_base64})

        return jsonify({"error": "Image not generated"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
