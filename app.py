import streamlit as st
from PIL import Image

from analyzer import analyze_with_ai
from rules import detect_signals
from risk_engine import calculate_risk
from url_checker import analyze_url
from screenshot_analyzer import extract_text_from_image


st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)

st.title("ScamShield")
st.subheader("AI-powered scam risk analysis")


message_tab, url_tab, screenshot_tab = st.tabs(
    ["Message Analysis", "URL Analysis", "Screenshot Analysis"]
)


# ==========================================================
# MESSAGE ANALYSIS
# ==========================================================

with message_tab:

    message = st.text_area(
        "Paste a suspicious message here",
        placeholder="Example: Your account will be blocked today. Click here to verify...",
        height=180
    )

    if st.button("Analyze Message", type="primary"):

        if message.strip():

            rule_score, signals = detect_signals(message)

            with st.spinner("Analyzing message..."):
                ai_analysis = analyze_with_ai(message)

            final_score, risk_level = calculate_risk(
                rule_score,
                ai_analysis
            )

            st.divider()

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

            st.subheader("AI Analysis")
            st.write(ai_analysis)

            st.subheader("Detected Signals")

            if signals:
                for signal in signals:
                    st.write("•", signal)
            else:
                st.write("No obvious scam signals detected.")

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


# ==========================================================
# URL ANALYSIS
# ==========================================================

with url_tab:

    st.write("Check a suspicious URL for common risk signals.")

    url = st.text_input(
        "Enter a URL",
        placeholder="Example: https://example.com/login"
    )

    if st.button("Analyze URL", type="primary"):

        if url.strip():

            url_score, url_signals = analyze_url(url)

            st.divider()

            if url_score >= 70:
                st.error(
                    f"URL RISK SCORE: {url_score}/100 — HIGH RISK"
                )

            elif url_score >= 40:
                st.warning(
                    f"URL RISK SCORE: {url_score}/100 — MEDIUM RISK"
                )

            else:
                st.success(
                    f"URL RISK SCORE: {url_score}/100 — LOW RISK"
                )

            st.subheader("Detected URL Signals")

            if url_signals:
                for signal in url_signals:
                    st.write("•", signal)
            else:
                st.write(
                    "No obvious suspicious URL patterns were detected."
                )

            st.subheader("Recommended Action")

            if url_score >= 70:
                st.write(
                    "Avoid opening this URL. Do not enter passwords, "
                    "OTP codes, banking information, or other sensitive data."
                )

            elif url_score >= 40:
                st.write(
                    "Be cautious with this URL. Verify the website "
                    "through an official source before continuing."
                )

            else:
                st.write(
                    "No major suspicious URL patterns were detected. "
                    "Still verify unexpected links before opening them."
                )

        else:
            st.warning("Please enter a URL first.")


# ==========================================================
# SCREENSHOT ANALYSIS
# ==========================================================

with screenshot_tab:

    st.write(
        "Upload a screenshot of a suspicious message. "
        "ScamShield will extract the text and analyze it."
    )

    uploaded_image = st.file_uploader(
        "Upload a screenshot",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image is not None:

        image = Image.open(uploaded_image)

        st.image(
            image,
            caption="Uploaded Screenshot",
            use_container_width=True
        )

        if st.button("Analyze Screenshot", type="primary"):

            with st.spinner("Reading screenshot..."):
                extracted_text = extract_text_from_image(image)

            if extracted_text:

                st.subheader("Extracted Text")

                st.text_area(
                    "Text detected from screenshot",
                    extracted_text,
                    height=150
                )

                screenshot_rule_score, screenshot_signals = detect_signals(
                    extracted_text
                )

                with st.spinner("Analyzing screenshot content..."):
                    screenshot_ai_analysis = analyze_with_ai(
                        extracted_text
                    )

                screenshot_score, screenshot_risk_level = calculate_risk(
                    screenshot_rule_score,
                    screenshot_ai_analysis
                )

                st.divider()

                if screenshot_risk_level == "HIGH":

                    st.error(
                        f"RISK SCORE: {screenshot_score}/100 — HIGH RISK"
                    )

                elif screenshot_risk_level == "MEDIUM":

                    st.warning(
                        f"RISK SCORE: {screenshot_score}/100 — MEDIUM RISK"
                    )

                else:

                    st.success(
                        f"RISK SCORE: {screenshot_score}/100 — LOW RISK"
                    )

                st.subheader("AI Analysis")
                st.write(screenshot_ai_analysis)

                st.subheader("Detected Signals")

                if screenshot_signals:

                    for signal in screenshot_signals:
                        st.write("•", signal)

                else:

                    st.write(
                        "No obvious scam signals detected."
                    )

                st.subheader("Recommended Action")

                if screenshot_risk_level == "HIGH":

                    st.write(
                        "Do not click suspicious links or share sensitive "
                        "information. Verify the request through an official "
                        "website or app."
                    )

                elif screenshot_risk_level == "MEDIUM":

                    st.write(
                        "Be cautious. Verify the sender and request through "
                        "an official channel before taking action."
                    )

                else:

                    st.write(
                        "No major risk signals were detected, but always "
                        "verify unexpected messages before responding."
                    )

            else:

                st.warning(
                    "No readable text was detected in the screenshot."
                )