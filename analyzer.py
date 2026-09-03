import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def analyze_with_ai(message):

    prompt = f"""
You are ScamShield, an AI cybersecurity assistant.

Analyze the following message for potential scam, phishing, or fraud signals.

MESSAGE:
{message}

Give your analysis in exactly this format:

Risk: LOW, MEDIUM, or HIGH

Why:
Give a clear explanation in 2-3 sentences. Mention the specific suspicious
patterns found in the message.

Advice:
Give 1-2 practical safety actions the user should take.

Important:
- Do not claim the message is definitely a scam.
- Use phrases such as "potential scam", "potentially suspicious", or "high-risk".
- Focus on observable evidence in the message.
- Do not invent information that is not present.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text