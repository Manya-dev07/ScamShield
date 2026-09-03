import streamlit as st
from analyzer import analyze_with_ai
from rules import detect_signals
from risk_engine import calculate_risk

st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)

st.title("ScamShield")
st.subheader("AI-powered scam risk analysis")

message = st.text_area(
    "Paste a suspicious message here",
    placeholder="Example: Your account will be blocked today. Click here to verify...",
    height=180
)

if st.button("Analyze", type="primary"):

    if message.strip():

        # Rule-based analysis
        rule_score, signals = detect_signals(message)

        # AI analysis
        with st.spinner("Analyzing message..."):
            ai_analysis = analyze_with_ai(message)

        # Final risk assessment
        final_score, risk_level = calculate_risk(
            rule_score,
            ai_analysis
        )

        st.divider()

        # Final risk result
        if risk_level == "HIGH":
            st.error(
                f"RISK SCORE: {final_score}/100 — HIGH RISK"
            )

        elif risk_level == "MEDIUM":
            st.warning(
                f"RISK SCORE: {final_score}/100 — MEDIUM RISK"
            )

        else:
            st.success(
                f"RISK SCORE: {final_score}/100 — LOW RISK"
            )

        # AI explanation
        st.subheader("AI Analysis")
        st.write(ai_analysis)

        # Detected signals
        st.subheader("Detected Signals")

        if signals:
            for signal in signals:
                st.write("•", signal)
        else:
            st.write("No obvious scam signals detected.")

        # Recommendation
        st.subheader("Recommended Action")

        if risk_level == "HIGH":
            st.write(
                "Do not click suspicious links or share sensitive information. "
                "Verify the request through the organization's official website or app."
            )

        elif risk_level == "MEDIUM":
            st.write(
                "Be cautious. Verify the sender and request through an official channel."
            )

        else:
            st.write(
                "No major risk signals were detected, but always verify unexpected requests."
            )

    else:
        st.warning("Please enter a message first.")