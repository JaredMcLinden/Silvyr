from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    print("📩 Message received:", user_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_reply = response.choices[0].message.content
    print("🤖 AI replied:", ai_reply)
    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    app.run(debug=True, port=5001)