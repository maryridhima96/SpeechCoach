from flask import Flask, render_template, request
import openai
import os

openai.api_key = "OPENAI_API_KEY"  # Your API key

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

import random

@app.route('/', methods=['GET', 'POST'])
def index():
    transcription = ""
    feedback = ""

    # 🎯 Random prompt list
    prompts = [
        "What does success mean to you?",
        "Describe a moment you felt truly proud.",
        "Talk about your favorite childhood memory.",
        "What is a habit that changed your life?",
        "Share your thoughts on technology and the future.",
        "What’s something you wish schools taught?",
        "If you could give your younger self advice, what would it be?",
        "What motivates you to keep going on tough days?",
        "What’s one thing the world needs more of?",
        "Describe a place that makes you feel at peace."
    ]
    random_prompt = random.choice(prompts)

    if request.method == 'POST':
        audio_file = request.files['audio']
        if audio_file:
            filepath = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(filepath)

            with open(filepath, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                )
                transcription = transcript.text

            prompt = f"""
You are a public speaking coach helping people improve their 1-minute speeches. Evaluate the following speech on 7 key criteria and give a score out of 10. Each category has its own max score:

1. Clarity of speech (2 points)
2. Pace and rhythm (2 points)
3. Filler word usage (1 point)
4. Pronunciation (1 point)
5. Sentence structure (1 point)
6. Confidence and energy (2 points)
7. Grammar and vocabulary (1 point)

**Instructions:**

- For each category, give a score and 1–2 short sentences of constructive feedback, especially when the score is less than full.
- Include specific examples or simple tips for improvement if relevant.
- Use a warm, encouraging tone — like a friendly mentor.
- After the breakdown, provide a **total score out of 10**.
- Finish with a short, motivating paragraph of overall feedback.

Here is the user's speech:

\"\"\"{transcription}\"\"\"
"""

            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful and insightful public speaking coach."},
                    {"role": "user", "content": prompt}
                ]
            )

            feedback = response.choices[0].message.content

    return render_template("index.html", transcription=transcription, feedback=feedback, speech_prompt=random_prompt)

if __name__ == '__main__':
    app.run(debug=True)
