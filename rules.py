def detect_signals(message):

    text = message.lower()

    signals = []
    score = 0

    # Urgency
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

    # Sensitive information
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

    # Financial context
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

    # Suspicious URL
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

    score = min(score, 100)

    return score, signals