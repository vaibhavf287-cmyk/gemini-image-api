import os
import requests
from flask import Flask, request

app = Flask(__name__)

# 🔴 Yahan apni DeepAI API key daalo
DEEPAI_API_KEY = "e00ff251-416d-41b2-b05e-c5ea692fe3e5"

@app.route("/")
def home():
    return """
    <h2>Simple Free Image Generator</h2>
    <form action="/generate" method="post">
        <input type="text" name="prompt" placeholder="Enter prompt"
        style="width:300px;height:40px;">
        <button type="submit" style="height:40px;">Generate</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.form.get("prompt")

    if not prompt:
        return "Please enter a prompt"

    response = requests.post(
        "https://api.deepai.org/api/text2img",
        data={"text": prompt},
        headers={"api-key": DEEPAI_API_KEY}
    )

    result = response.json()

    if "output_url" not in result:
        return f"Error: {result}"

    image_url = result["output_url"]

    return f"""
    <h3>Generated Image:</h3>
    <img src="{image_url}" width="512"/>
    <br><br>
    <a href="/">Generate Another</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
