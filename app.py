import os
import requests
import base64
from flask import Flask, request

app = Flask(__name__)

# 🔴 YAHAN APNA TOKEN DALO
HF_TOKEN = "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"

API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return """
    <h2>Free AI Image Generator</h2>
    <form action="/generate" method="post">
        <input type="text" name="prompt" placeholder="Enter prompt"
        style="width:300px;height:35px;">
        <button type="submit">Generate</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")

    if not prompt:
        return "Enter prompt"

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    image_base64 = base64.b64encode(response.content).decode("utf-8")

    return f"""
    <h3>Generated Image:</h3>
    <img src="data:image/png;base64,{image_base64}" width="500"/>
    <br><br>
    <a href="/">Generate Another</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
t=port)

