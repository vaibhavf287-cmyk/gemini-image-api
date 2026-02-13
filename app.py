import os
import requests
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

MODEL_VERSION = "7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc"

@app.route("/")
def home():
    return "SDXL Image API Running"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "version": MODEL_VERSION,
        "input": {
            "prompt": prompt,
            "width": 768,
            "height": 768,
            "num_inference_steps": 25
        }
    }

    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json=payload
    )

    prediction = response.json()

    if "id" not in prediction:
        return jsonify(prediction)

    prediction_id = prediction["id"]

    while True:
        time.sleep(2)
        check = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers=headers
        )
        result = check.json()

        if result["status"] == "succeeded":
            return jsonify({
                "image_url": result["output"][0]
            })

        if result["status"] == "failed":
            return jsonify(result)
