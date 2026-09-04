import streamlit as st
from PIL import Image

from analyzer import analyze_with_ai
from rules import detect_signals
from url_checker import analyze_url
from screenshot_analyzer import extract_text_from_image


st.set_page_config(
    page_title="ScamShield",
    page_icon="🛡️",
    layout="centered"
)


st.title("ScamShield")
st.subheader("AI-powered scam risk analysis")


# Create tabs
message_tab, url_tab, screenshot_tab = st.tabs(
    ["📩 Message Analysis", "🔗 URL Analysis", "📸 Screenshot Analysis"]
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

            # Rule-based analysis
            score, signals = detect_signals(message)

            # AI analysis
            with st.spinner("Analyzing message..."):
                ai_analysis = analyze_with_ai(message)

            st.divider()

            # Risk level
            if score >= 70:
                st.error(f"RISK SCORE: {score}/100 — HIGH RISK")

            elif score >= 40:
                st.warning(f"RISK SCORE: {score}/100 — MEDIUM RISK")

            else:
                st.success(f"RISK SCORE: {score}/100 — LOW RISK")

            # AI Analysis
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

            # Analyze URL
            url_score, url_signals = analyze_url(url)

            st.divider()

            # Risk level
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

            # Detected signals
            st.subheader("Detected URL Signals")

            if url_signals:
                for signal in url_signals:
                    st.write("•", signal)
            else:
                st.write(
                    "No obvious suspicious URL patterns were detected."
                )

            # Recommendation
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

        # Open uploaded image
        image = Image.open(uploaded_image)

        # Display screenshot
        st.image(
            image,
            caption="Uploaded Screenshot",
            use_container_width=True
        )

        if st.button("Analyze Screenshot", type="primary"):

            with st.spinner("Reading screenshot..."):

                # Extract text using OCR
                extracted_text = extract_text_from_image(image)

            if extracted_text:

                # Show extracted text
                st.subheader("Extracted Text")
                st.text_area(
                    "Text detected from screenshot",
                    extracted_text,
                    height=150
                )

                # Analyze extracted text using existing rules
                screenshot_score, screenshot_signals = detect_signals(
                    extracted_text
                )

                # Analyze extracted text using existing AI
                with st.spinner("Analyzing screenshot content..."):
                    screenshot_ai_analysis = analyze_with_ai(
                        extracted_text
                    )

                st.divider()

                # Risk level
                if screenshot_score >= 70:

                    st.error(
                        f"RISK SCORE: {screenshot_score}/100 — HIGH RISK"
                    )

                elif screenshot_score >= 40:

                    st.warning(
                        f"RISK SCORE: {screenshot_score}/100 — MEDIUM RISK"
                    )

                else:

                    st.success(
                        f"RISK SCORE: {screenshot_score}/100 — LOW RISK"
                    )

                # AI Analysis
                st.subheader("AI Analysis")
                st.write(screenshot_ai_analysis)

                # Detected signals
                st.subheader("Detected Signals")

                if screenshot_signals:

                    for signal in screenshot_signals:
                        st.write("•", signal)

                else:

                    st.write(
                        "No obvious scam signals detected."
                    )

                # Recommendation
                st.subheader("Recommended Action")

                if screenshot_score >= 70:

                    st.write(
                        "Do not click suspicious links or share sensitive "
                        "information. Verify the request through an official "
                        "website or app."
                    )

                elif screenshot_score >= 40:

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