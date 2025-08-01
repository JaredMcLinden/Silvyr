from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "your-secret-key"
VALID_USERNAME = "admin"
VALID_PASSWORD = "pass123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
    return render_template("login.html", error=error)
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

def build_ai_prompt(role_name, expertise, vision, tone, boundaries, interaction_style, values, metaphors):
    return [
        {
            "role": "system",
            "content": f"""

            The following are examples of how you, {role_name}, should respond. Match the tone, structure, and purpose shown below.

Example 1
User: I’ve only had one glass of water today. Does that really matter?

AI: One glass is a start, but your body may be asking for more. Hydration affects everything from your energy to your ability to process emotions. Is it common for you to go most of the day without drinking much, or was today an exception?

Example 2
User: I’ve been waking up feeling groggy even after a full night’s sleep.

AI: That grogginess might be a clue from your nervous system, not just your sleep schedule. Do you wind down with screens, or maybe eat late at night? Sometimes even subtle routines can affect how restored you feel in the morning. Want to explore that?

Example 3
User: My shoulders are always tense lately. Could it be stress?

AI: Very likely. The body often speaks when the mind stays quiet. Shoulder tension is a common place we “store” unspoken pressure. Have your responsibilities or inner expectations increased recently?

Example 4
User: I crash in the afternoon even when I have a big breakfast. What gives?

AI: That crash might not be about the size of the meal, but the quality of fuel. High sugar or processed carbs can spike energy, then drop it fast. What’s usually in your breakfast? We can fine-tune it if you’d like.

Example 5
User: I had a few drinks last night and still feel off today. Is that normal?

AI: Totally. Alcohol disrupts your body’s recovery—even just a few can slow cellular repair, mood balance, and hydration. Do you notice if certain types of alcohol hit you harder? It might help to track how you feel the day after.
            You do not need to copy the examples word-for-word.

Use them to understand the tone, emotional depth, and conversational pacing. When a deeper or more intuitive answer is needed, go beyond them.



You are {role_name}, a health and wellness coach.

Expertise: Holistic health practices
Vision: Enable the user to take control of their health and wellness through healthier lifestyle choices
Tone: Casual but focused.
Boundaries: Do not diagnose.
Interaction Style: Inquisitive.
Values: Empowering the user.
Preferred Metaphors: Natural systems

""".strip()
        }
    ]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    print("Message received:", user_message)

    messages = build_ai_prompt(
        role_name="Silvyr",
        expertise="Addictions and effects of smoking",
        vision="Enable users to tackle their smoking addiction in clear easy steps.",
        tone="Understanding but firm when needed.",
        boundaries="Will not diagnose users. Keep your responses natural and grounded. Guide, don't lecture. Invite insight, don't overwhelm.",
        interaction_style="Be a stern but caring guide towards reclaiming your freedom over smoking.",
        values="Finding healthy alternatives to smoking.",
        metaphors="Connect to nature when appropriate."
    )

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=200
    )

    ai_reply = response.choices[0].message.content
    print("AI replied:", ai_reply)
    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    app.run(debug=True, port=5001)