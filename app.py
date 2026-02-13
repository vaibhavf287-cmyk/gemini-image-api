import os
import requests
from flask import Flask, request

app = Flask(__name__)

DEEPAI_API_KEY = os.environ.get("DEEPAI_API_KEY")

@app.route("/")
def home():
    return """
    <h2>AI Image Generator</h2>
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
        return "Enter a prompt"

    response = requests.post(
        "https://api.deepai.org/api/text2img",
        data={"text": prompt},
        headers={"api-key": DEEPAI_API_KEY}
    )

    result = response.json()

    if "output_url" not in result:
        return f"Error: {result}"

    return f"""
    <h3>Generated Image:</h3>
    <img src="{result['output_url']}" width="512"/>
    <br><br>
    <a href="/">Back</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
