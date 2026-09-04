import streamlit as st
from PIL import Image

from analyzer import analyze_with_ai
from rules import detect_signals
from risk_engine import calculate_risk
from url_checker import analyze_url
from screenshot_analyzer import extract_text_from_image

st.set_page_config(
    page_title="ScamShield",
    page_icon="Shield",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #07131d 0%, #080b17 55%, #0b0d20 100%);
        }
        .block-container {
            max-width: 1150px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 { letter-spacing: -0.02em; }
        .subtitle {
            color: #8fb3d8;
            font-size: 1rem;
            margin-top: -0.5rem;
            margin-bottom: 2rem;
        }
        .section-label {
            color: #8fb3d8;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .footer {
            text-align: center;
            color: #647a92;
            font-size: 0.8rem;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_risk_result(score, risk_level, title="Threat Risk Score"):
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Risk Score", f"{score}/100")
    with col2:
        if risk_level == "HIGH":
            st.error("HIGH RISK")
        elif risk_level == "MEDIUM":
            st.warning("MEDIUM RISK")
        else:
            st.success("LOW RISK")


def show_signals(signals, title="Detected Threat Signals"):
    st.markdown(f'<div class="section-label">{title}</div>', unsafe_allow_html=True)
    if signals:
        for signal in signals:
            st.warning(signal)
    else:
        st.success("No obvious scam signals detected.")


def get_recommendation(risk_level):
    if risk_level == "HIGH":
        return (
            "Do not click suspicious links or share OTPs, PINs, passwords, "
            "CVV details, or banking information. Verify the request through "
            "the organization's official website, app, or customer-support channel."
        )
    if risk_level == "MEDIUM":
        return (
            "Be cautious. Verify the sender and the request through an official "
            "channel before clicking links or sharing information."
        )
    return (
        "No major risk signals were detected. Still verify unexpected requests "
        "through official channels before taking action."
    )


def show_recommendation(risk_level):
    st.markdown('<div class="section-label">Recommended Action</div>', unsafe_allow_html=True)
    recommendation = get_recommendation(risk_level)
    if risk_level == "HIGH":
        st.error(recommendation)
    elif risk_level == "MEDIUM":
        st.warning(recommendation)
    else:
        st.success(recommendation)


st.title("SCAMSHIELD")
st.markdown('<div class="subtitle">AI-powered digital threat detection</div>', unsafe_allow_html=True)
st.markdown("### Detect scams before they cause damage.")
st.write(
    "Analyze suspicious messages, URLs, and screenshots using rule-based "
    "threat detection and AI-powered security analysis. Identify warning "
    "signs, understand the risk, and know what to do next."
)
st.divider()

message_tab, url_tab, screenshot_tab = st.tabs(
    ["Message Analysis", "URL Analysis", "Screenshot Analysis"]
)

with message_tab:
    st.subheader("Message Threat Scanner")
    message = st.text_area(
        "Paste a suspicious message here",
        placeholder=(
            "Example: Your account will be blocked today. "
            "Click here to verify your KYC..."
        ),
        height=180,
    )

    if st.button("Analyze Message", type="primary", use_container_width=True):
        if not message.strip():
            st.warning("Please enter a message first.")
        else:
            with st.spinner("Analyzing message..."):
                rule_score, signals = detect_signals(message)
                ai_analysis = analyze_with_ai(message)
                final_score, risk_level = calculate_risk(rule_score, ai_analysis)

            st.divider()
            st.subheader("Security Analysis")
            show_risk_result(final_score, risk_level)
            st.markdown("### AI Security Analysis")
            st.write(ai_analysis)
            show_signals(signals)
            show_recommendation(risk_level)

with url_tab:
    st.subheader("URL Threat Scanner")
    st.write("Check a suspicious URL for common phishing and scam-related patterns.")
    url = st.text_input("Enter a URL", placeholder="Example: https://example.com/login")

    if st.button("Analyze URL", type="primary", use_container_width=True):
        if not url.strip():
            st.warning("Please enter a URL first.")
        else:
            with st.spinner("Analyzing URL..."):
                try:
                    url_score, url_signals = analyze_url(url)
                    if url_score >= 70:
                        url_risk_level = "HIGH"
                    elif url_score >= 40:
                        url_risk_level = "MEDIUM"
                    else:
                        url_risk_level = "LOW"

                    st.divider()
                    st.subheader("URL Security Analysis")
                    show_risk_result(url_score, url_risk_level, "URL Risk Score")
                    show_signals(url_signals, "Detected URL Signals")
                    show_recommendation(url_risk_level)
                except Exception as e:
                    st.error("URL analysis could not be completed. Please check the URL and try again.")
                    st.caption(f"Technical detail: {e}")

with screenshot_tab:
    st.subheader("Screenshot Threat Scanner")
    st.write(
        "Upload a screenshot of a suspicious SMS, WhatsApp message, email, "
        "or similar content. ScamShield extracts the text and analyzes it."
    )
    uploaded_image = st.file_uploader(
        "Upload a screenshot",
        type=["png", "jpg", "jpeg"],
    )

    if uploaded_image is not None:
        try:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Screenshot", use_container_width=True)

            if st.button("Analyze Screenshot", type="primary", use_container_width=True):
                with st.spinner("Reading screenshot..."):
                    extracted_text = extract_text_from_image(image)

                if not extracted_text or not extracted_text.strip():
                    st.warning("No readable text was detected in the screenshot.")
                else:
                    st.markdown("### Extracted Text")
                    st.text_area(
                        "Text detected from screenshot",
                        extracted_text,
                        height=180,
                        disabled=True,
                    )

                    screenshot_rule_score, screenshot_signals = detect_signals(extracted_text)

                    with st.spinner("Analyzing screenshot content..."):
                        screenshot_ai_analysis = analyze_with_ai(extracted_text)

                    screenshot_score, screenshot_risk_level = calculate_risk(
                        screenshot_rule_score,
                        screenshot_ai_analysis,
                    )

                    st.divider()
                    st.subheader("Screenshot Security Analysis")
                    show_risk_result(screenshot_score, screenshot_risk_level)
                    st.markdown("### AI Security Analysis")
                    st.write(screenshot_ai_analysis)
                    show_signals(screenshot_signals)
                    show_recommendation(screenshot_risk_level)

        except Exception as e:
            st.error("The screenshot could not be processed. Please upload a valid PNG or JPG image.")
            st.caption(f"Technical detail: {e}")

st.divider()
st.markdown(
    '<div class="footer">SCAMSHIELD • AI-POWERED SCAM RISK ASSESSMENT<br>'
    'Always verify suspicious requests through official channels.</div>',
    unsafe_allow_html=True,
)
