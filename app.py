import streamlit as st
from rules import detect_signals

st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)

st.title("ScamShield")
st.subheader("AI-powered scam risk analysis")

message = st.text_area(
    "Paste a suspicious message here",
    placeholder="Example: Your account will be blocked today. Click here to verify..."
)


def analyze_message(message):

    text = message.lower()

    signals = []
    score = 0

    # 1. Urgency detection
    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "today",
        "blocked",
        "expires"
    ]

    if any(word in text for word in urgency_words):
        signals.append("Artificial urgency detected")
        score += 20

    # 2. Sensitive information detection
    sensitive_words = [
        "otp",
        "pin",
        "password",
        "kyc",
        "cvv",
        "account number"
    ]

    if any(word in text for word in sensitive_words):
        signals.append("Sensitive information requested")
        score += 20

    # 3. Financial context detection
    financial_words = [
        "bank",
        "upi",
        "payment",
        "refund",
        "money",
        "account"
    ]

    if any(word in text for word in financial_words):
        signals.append("Financial context detected")
        score += 15

    # 4. Suspicious URL detection
    if "http://" in text or "https://" in text or "www." in text:

        suspicious_patterns = [
            ".xyz",
            ".tk",
            ".ml",
            ".ga",
            "verify",
            "kyc",
            "login"
        ]

        if any(pattern in text for pattern in suspicious_patterns):
            signals.append("Potentially suspicious URL detected")
            score += 30

    # Make sure score never goes above 100
    score = min(score, 100)

    return score, signals


if st.button("Analyze"):

    if message.strip():

        score, signals = analyze_message(message)

        st.divider()

        # Risk level
        if score >= 70:
            st.error(f"RISK SCORE: {score}/100 — HIGH RISK")

        elif score >= 40:
            st.warning(f"RISK SCORE: {score}/100 — MEDIUM RISK")

        else:
            st.success(f"RISK SCORE: {score}/100 — LOW RISK")

        # Signals
        st.subheader("Detected Signals")

        if signals:
            for signal in signals:
                st.write("•", signal)
        else:
            st.write("No obvious scam signals detected.")

        # Recommendation
        st.subheader("Recommended Action")

        if score >= 70:
            st.write(
                "Do not click suspicious links or share sensitive information. "
                "Verify the request through the organization's official website or app."
            )

        elif score >= 40:
            st.write(
                "Be cautious. Verify the sender and request through an official channel."
            )

        else:
            st.write(
                "No major risk signals were detected, but always verify unexpected requests."
            )

    else:
        st.warning("Please enter a message first.")