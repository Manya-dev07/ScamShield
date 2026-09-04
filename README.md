# ScamShield

### Check before you click.

ScamShield is an AI-powered cybersecurity platform that analyzes suspicious messages, URLs, and screenshots to identify potential scam and phishing signals.

Instead of simply labeling content as "safe" or "scam", ScamShield provides a risk score, explains the detected warning signs, and recommends practical safety actions.

## Features

- Message Analysis
  - Analyzes suspicious messages using AI and rule-based detection.
  - Detects signals such as urgency, requests for sensitive information, financial context, and suspicious links.

- URL Security Analysis
  - Examines URLs for potentially suspicious patterns.
  - Checks for HTTP usage, suspicious keywords, unusual domains, IP-based URLs, URL shorteners, punycode, and other indicators.

- Screenshot Analysis
  - Extracts text from uploaded screenshots using OCR.
  - Runs the extracted content through the same rule-based and AI analysis pipeline.

- Explainable Risk Assessment
  - Generates a risk score from 0–100.
  - Classifies the result as LOW, MEDIUM, or HIGH risk.
  - Shows the specific signals detected.
  - Provides practical safety recommendations.

## How It Works

User Input
    |
    v
Message / URL / Screenshot
    |
    v
Input Processing
    |
    +-------------------+
    |                   |
    v                   v
Rule Engine         AI Analysis
    |                   |
    +---------+---------+
              |
              v
         Risk Engine
              |
              v
    Risk Score + Explanation
              |
              v
      Safety Recommendation

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- Python rule-based detection
- Tesseract OCR
- Pillow
- python-dotenv

## Project Structure

    ScamShield/
    |
    ├── app.py
    ├── analyzer.py
    ├── rules.py
    ├── url_checker.py
    ├── risk_engine.py
    ├── screenshot_analyzer.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore

## Installation

### 1. Clone the repository

    git clone https://github.com/Manya-dev07/ScamShield.git

    cd ScamShield

### 2. Install Python dependencies

    pip install -r requirements.txt

### 3. Configure the Gemini API key

Create a `.env` file in the project folder:

    GEMINI_API_KEY=your_api_key_here

Do not share or commit your API key.

### 4. Install Tesseract OCR

Screenshot analysis requires the Tesseract OCR engine to be installed on the system.

After installation, make sure the Tesseract executable is available in the system PATH.

### 5. Run ScamShield

    streamlit run app.py

The application will open in your browser.

## Risk Assessment

ScamShield combines rule-based signals with AI analysis to produce a risk assessment.

Examples of detected signals include:

- Artificial urgency
- Requests for sensitive information
- Financial context
- Suspicious URLs
- Unusual domain patterns
- URL shorteners
- IP-based URLs
- Punycode domains

The system is designed as a decision-support tool and does not claim that every flagged message or URL is definitively fraudulent.

## Team

### Neural Ninjas

- Manya
- Madhu Bhardwaj
- Aahna Kurrey

## Project Goal

ScamShield aims to help users recognize potential scams before they click suspicious links or share sensitive information.

### Safer decisions start before the click.