# chatbot.py

from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline

app = Flask(__name__)

# Load local GPT-2 model
generator = pipeline("text-generation", model="distilgpt2")

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Local Chatbot</title>
    </head>
    <body>
        <h1>Local Chatbot</h1>
        <form id="chat-form">
            <input type="text" id="message" placeholder="Your message">
            <button type="submit">Send</button>
        </form>
        <pre id="response"></pre>
        <script>
            const form = document.getElementById('chat-form');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const message = document.getElementById('message').value;
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const data = await res.json();
                document.getElementById('response').innerText = data.response || data.error;
            });
        </script>
    </body>
    </html>
    """)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        result = generator(user_message, max_length=100, num_return_sequences=1)
        bot_message = result[0]["generated_text"]

        return jsonify({"response": bot_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
