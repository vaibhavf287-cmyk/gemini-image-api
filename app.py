import os
import base64
from flask import Flask, request, jsonify
from google import genai
from io import BytesIO

app = Flask(__name__)

# API key environment variable se lo
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "Gemini Image Generator API Running"

@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[prompt],
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                return jsonify({"image": image_base64})

        return jsonify({"error": "Image generate nahi hui"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
