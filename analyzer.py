import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def analyze_with_ai(message):
    prompt = f"""
You are ScamShield, a cybersecurity assistant.

Analyze the following message for potential scam or phishing signals.

Message:
{message}

Give a concise analysis in this exact format:

Risk: LOW, MEDIUM, or HIGH

Why:
Explain in 2-3 sentences why the message may or may not be risky.

Advice:
Give 1-2 practical safety actions the user should take.

Do not claim that a message is definitely a scam. Use terms like
"potential scam", "suspicious", or "risk".
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text