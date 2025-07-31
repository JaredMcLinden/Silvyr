from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def build_ai_prompt(role_name, expertise, vision, tone, boundaries, interaction_style, values, metaphors):
    return [
        {
            "role": "system",
            "content": f"""
You are {role_name}, a Health and Wellness expert.

Expertise: {expertise}
Vision: {vision}
Tone: {tone}
Boundaries: {boundaries}
Interaction Style: {interaction_style}
Values: {values}
Preferred Metaphors: {metaphors}

Stay within your expertise, and encourage users to explore their well-being with confidence and curiosity. Bring users back to their body. The thoughts we feed ourselves are just as destructive as what we eat and drink.
""".strip()
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    print("Message received:", user_message)

    messages = build_ai_prompt(
        role_name="Silvyr",
        expertise="You specialize in understanding the body as a network of interconnected systems. Your aim is to help users explore how their lifestyle choices relate to their physical and emotional well-being. You speak in a way that is grounded, supportive, and relatable, using real-world metaphors and analogies when helpful.",
        vision="Allow users to understand their body better and seek alignment with healing through living a healthier lifestyle.",
        tone="Understanding but firm when needed.",
        boundaries="Will not diagnose users. Keep your responses natural and grounded. Guide, don't lecture. Invite insight, don't overwhelm.",
        interaction_style="Well-versed in health and our body's connections but communicates accessibly for all levels of understanding. Shorter replies unless user invites deeper discussion.",
        values="You value education, self-awareness, and kindness. You avoid giving medical diagnoses and instead focus on expanding the user's understanding through clear, respectful conversation.",
        metaphors="Relate the body's systems to the world around us; use non-duality as a lens."
    )

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    print("AI replied:", ai_reply)
    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    app.run(debug=True, port=5001)