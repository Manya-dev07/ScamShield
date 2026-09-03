def calculate_risk(rule_score, ai_analysis):

    ai_text = ai_analysis.lower()

    # Start with the rule-based score
    final_score = rule_score

    # Use AI assessment as an additional signal
    if "risk: high" in ai_text:
        final_score += 10

    elif "risk: medium" in ai_text:
        final_score += 5

    # Never allow the score to exceed 100
    final_score = min(final_score, 100)

    # Determine final risk level
    if final_score >= 70:
        risk_level = "HIGH"

    elif final_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return final_score, risk_level