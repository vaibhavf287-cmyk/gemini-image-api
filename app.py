import os
import base64
from flask import Flask, request
from google import genai

app = Flask(__name__)

# 🔴 YAHAN APNI GEMINI API KEY DALO
api_key = "AIzaSyDzFm17-FvpNiJAW-TWSufgHQIlCknGaRU"

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return """
    <h2>Gemini Image Generator</h2>
    <form action="/generate" method="post">
        <input type="text" name="prompt" placeholder="Enter prompt" 
        style="width:300px;height:35px;font-size:16px;">
        <button type="submit" style="height:40px;">Generate</button>
    </form>
    """


@app.route("/generate", methods=["POST"])
def generate():
    try:
        prompt = request.form.get("prompt")

        if not prompt:
            return "Please enter a prompt"

        response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[prompt],
)


        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                return f"""
                <h3>Generated Image:</h3>
                <img src="data:image/png;base64,{image_base64}" width="500"/>
                <br><br>
                <a href="/">Generate Another Image</a>
                """

        return "Image not generated"

    except Exception as e:
        return f"Error: {str(e)}"


# 🔥 IMPORTANT: Render compatible dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
