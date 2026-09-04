import streamlit as st
from PIL import Image

from analyzer import analyze_with_ai
from rules import detect_signals
from risk_engine import calculate_risk
from url_checker import analyze_url
from screenshot_analyzer import extract_text_from_image


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ScamShield",
    page_icon="Shield",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown(
    """
<style>

/* =========================
   MAIN BACKGROUND
   ========================= */

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(0, 153, 255, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(91, 70, 220, 0.13),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #040a12 0%,
            #07111c 48%,
            #080b18 100%
        );
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =========================
   GLOBAL TEXT
   ========================= */

html,
body,
.stApp {
    color: #eaf3ff !important;
}

p,
label,
.stMarkdown,
.stText,
.stCaption {
    color: #c1d0df;
}

h1,
h2,
h3,
h4 {
    color: #edf6ff !important;
    letter-spacing: -0.025em;
}

h2,
h3 {
    font-weight: 750 !important;
}


/* =========================
   HERO
   ========================= */

.hero {
    padding: 1.2rem 0 1.1rem 0;
}

.hero-kicker {
    color: #5db7ff;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}

.hero-title {
    color: #f4f9ff;
    font-size: 3.35rem;
    line-height: 1;
    font-weight: 850;
    letter-spacing: -0.055em;
    margin: 0;
}

.hero-title span {
    color: #55aaff;
}

.hero-subtitle {
    color: #9eb6ce;
    font-size: 1rem;
    line-height: 1.65;
    max-width: 850px;
    margin-top: 0.85rem;
}

.hero-line {
    height: 1px;
    margin-top: 1.45rem;
    background: linear-gradient(
        90deg,
        rgba(77, 176, 255, 0.75),
        rgba(77, 176, 255, 0.12),
        transparent
    );
}


/* =========================
   FEATURE CARDS
   ========================= */

.feature-box {
    background: linear-gradient(
        145deg,
        rgba(10, 28, 46, 0.9),
        rgba(7, 19, 33, 0.8)
    );

    border: 1px solid rgba(80, 166, 235, 0.22);
    border-radius: 13px;

    padding: 0.85rem 1rem;
    min-height: 72px;

    box-shadow:
        0 8px 25px rgba(0, 0, 0, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 0.025);
}

.feature-title {
    color: #eaf5ff;
    font-size: 0.86rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    text-align: center;
}

.feature-text {
    color: #7899b8;
    font-size: 0.7rem;
    margin-top: 0.22rem;
    text-align: center;
}


/* =========================
   SECTION LABEL
   ========================= */

.section-label {
    color: #5db7ff !important;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}


/* =========================
   TABS
   ========================= */

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;

    background: rgba(4, 13, 23, 0.78);

    padding: 0.35rem;

    border-radius: 12px;

    border: 1px solid rgba(82, 157, 219, 0.15);
}

.stTabs [data-baseweb="tab"] {
    height: 45px;

    border-radius: 9px;

    padding: 0 1.2rem;

    color: #7890a8 !important;

    font-weight: 700;
}

.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(
        135deg,
        rgba(39, 133, 220, 0.25),
        rgba(65, 92, 210, 0.18)
    );

    color: #eef7ff !important;
}

.stTabs [aria-selected="true"] p {
    color: #eef7ff !important;
}


/* =========================
   INPUTS
   ========================= */

.stTextArea textarea,
.stTextInput input {

    background: #081522 !important;

    color: #f1f7ff !important;

    -webkit-text-fill-color: #f1f7ff !important;

    border: 1px solid rgba(92, 168, 235, 0.28) !important;

    border-radius: 11px !important;

    caret-color: #62b5ff !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {

    border-color: #4eaeff !important;

    box-shadow:
        0 0 0 1px rgba(78, 174, 255, 0.3),
        0 0 20px rgba(40, 140, 230, 0.08) !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {

    color: #718aa3 !important;

    -webkit-text-fill-color: #718aa3 !important;

    opacity: 1 !important;
}


/* =========================
   FILE UPLOADER
   ========================= */

[data-testid="stFileUploader"] {

    background: rgba(7, 20, 34, 0.72);

    border: 1px dashed rgba(88, 166, 226, 0.32);

    border-radius: 12px;

    padding: 0.4rem;
}

[data-testid="stFileUploader"] label {
    color: #c5d7e8 !important;
}


/* =========================
   BUTTONS
   ========================= */

.stButton > button {

    min-height: 44px;

    border-radius: 9px;

    font-weight: 800;

    color: #f3f9ff;

    border: 1px solid rgba(91, 171, 240, 0.38);

    background: linear-gradient(
        135deg,
        #1676c8,
        #2859b8
    );

    box-shadow:
        0 5px 18px rgba(20, 100, 190, 0.18);
}

.stButton > button:hover {

    border-color: rgba(117, 195, 255, 0.7);

    box-shadow:
        0 7px 22px rgba(30, 130, 230, 0.24);
}


/* =========================
   METRIC / RISK SCORE
   ========================= */

[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            rgba(9, 27, 45, 0.95),
            rgba(7, 18, 31, 0.9)
        );

    border: 1px solid rgba(83, 164, 226, 0.22);

    border-radius: 13px;

    padding: 1rem 1.1rem;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.025);
}

[data-testid="stMetricLabel"] {

    color: #7fa1c0 !important;

    font-weight: 700 !important;
}

[data-testid="stMetricValue"] {

    color: #f3f8ff !important;

    font-weight: 800 !important;
}


/* =========================
   ALERT BOX TEXT
   ========================= */

div[data-testid="stAlert"] p {

    color: inherit !important;

    font-weight: 600;
}


/* =========================
   AI ANALYSIS BOX
   ========================= */

div[data-testid="stAlert"][data-baseweb="notification"] {

    border-radius: 11px;
}


/* =========================
   DIVIDERS
   ========================= */

hr {

    border-color: rgba(92, 161, 220, 0.13) !important;
}


/* =========================
   IMAGE
   ========================= */

[data-testid="stImage"] img {

    border-radius: 11px;

    border: 1px solid rgba(91, 163, 224, 0.2);
}


/* =========================
   INFO CARD
   ========================= */

.info-card {

    background:
        linear-gradient(
            145deg,
            rgba(10, 28, 46, 0.86),
            rgba(7, 18, 32, 0.78)
        );

    border: 1px solid rgba(82, 161, 224, 0.18);

    border-radius: 12px;

    padding: 1.1rem;

    margin-top: 1rem;
}

.info-title {

    color: #dceeff;

    font-weight: 800;

    font-size: 0.82rem;

    letter-spacing: 0.06em;
}

.info-text {

    color: #86a4bf;

    font-size: 0.8rem;

    line-height: 1.55;

    margin-top: 0.35rem;
}


/* =========================
   FOOTER
   ========================= */

.footer {

    text-align: center;

    color: #58718b;

    font-size: 0.7rem;

    line-height: 1.7;

    padding-top: 1.2rem;

    letter-spacing: 0.05em;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def show_risk_result(score, risk_level, title="Threat Risk Score"):

    st.markdown(
        f'<div class="section-label">{title}</div>',
        unsafe_allow_html=True,
    )

    score_col, risk_col = st.columns([1, 1])

    with score_col:
        st.metric(
            "RISK SCORE",
            f"{score}/100",
        )

    with risk_col:

        if risk_level == "HIGH":
            st.error("HIGH RISK")

        elif risk_level == "MEDIUM":
            st.warning("MEDIUM RISK")

        else:
            st.success("LOW RISK")


def show_signals(
    signals,
    title="Detected Threat Signals",
):

    st.markdown(
        f'<div class="section-label">{title}</div>',
        unsafe_allow_html=True,
    )

    if signals:

        for signal in signals:
            st.warning(signal)

    else:

        st.success(
            "No obvious scam signals detected."
        )


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

    st.markdown(
        '<div class="section-label">Recommended Action</div>',
        unsafe_allow_html=True,
    )

    recommendation = get_recommendation(
        risk_level
    )

    if risk_level == "HIGH":

        st.error(recommendation)

    elif risk_level == "MEDIUM":

        st.warning(recommendation)

    else:

        st.success(recommendation)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">

<div class="hero-kicker">
AI SECURITY • THREAT INTELLIGENCE
</div>

<div class="hero-title">
SCAM<span>SHIELD</span>
</div>

<div class="hero-subtitle">
Analyze suspicious messages, URLs, and screenshots using AI-powered
security analysis and rule-based threat detection. Understand the warning
signs, assess the risk, and know what action to take before you click.
</div>

<div class="hero-line"></div>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# FEATURE STRIP
# =========================================================

f1, f2, f3, f4 = st.columns(4)

with f1:

    st.markdown(
        """
<div class="feature-box">
<div class="feature-title">MESSAGE</div>
<div class="feature-text">AI + rule analysis</div>
</div>
""",
        unsafe_allow_html=True,
    )

with f2:

    st.markdown(
        """
<div class="feature-box">
<div class="feature-title">URL</div>
<div class="feature-text">Phishing pattern checks</div>
</div>
""",
        unsafe_allow_html=True,
    )

with f3:

    st.markdown(
        """
<div class="feature-box">
<div class="feature-title">SCREENSHOT</div>
<div class="feature-text">OCR + threat analysis</div>
</div>
""",
        unsafe_allow_html=True,
    )

with f4:

    st.markdown(
        """
<div class="feature-box">
<div class="feature-title">EXPLAINABLE</div>
<div class="feature-text">Risk + reasons + action</div>
</div>
""",
        unsafe_allow_html=True,
    )


st.write("")


# =========================================================
# TABS
# =========================================================

message_tab, url_tab, screenshot_tab = st.tabs(
    [
        "Message Analysis",
        "URL Analysis",
        "Screenshot Analysis",
    ]
)


# =========================================================
# MESSAGE ANALYSIS
# =========================================================

with message_tab:

    st.subheader("Message Threat Scanner")

    st.write(
        "Paste a suspicious SMS, email, payment request, "
        "or social-media message."
    )

    message = st.text_area(
        "Suspicious message",
        placeholder=(
            "Example: Your account will be blocked today. "
            "Click here to verify your KYC..."
        ),
        height=170,
        label_visibility="collapsed",
    )

    if st.button(
        "Analyze Message",
        type="primary",
        width="stretch",
    ):

        if not message.strip():

            st.warning(
                "Please enter a message first."
            )

        else:

            with st.spinner(
                "Analyzing message..."
            ):

                rule_score, signals = (
                    detect_signals(message)
                )

                ai_analysis = (
                    analyze_with_ai(message)
                )

                final_score, risk_level = (
                    calculate_risk(
                        rule_score,
                        ai_analysis,
                    )
                )

            st.divider()

            st.subheader(
                "Security Analysis"
            )

            show_risk_result(
                final_score,
                risk_level,
            )

            st.markdown(
                "### AI Security Analysis"
            )

            st.info(ai_analysis)

            show_signals(
                signals
            )

            show_recommendation(
                risk_level
            )


# =========================================================
# URL ANALYSIS
# =========================================================

with url_tab:

    st.subheader(
        "URL Threat Scanner"
    )

    st.write(
        "Check a suspicious URL for common "
        "phishing and scam-related patterns."
    )

    url = st.text_input(
        "Suspicious URL",
        placeholder=(
            "Example: https://example.com/login"
        ),
        label_visibility="collapsed",
    )

    if st.button(
        "Analyze URL",
        type="primary",
        width="stretch",
    ):

        if not url.strip():

            st.warning(
                "Please enter a URL first."
            )

        else:

            with st.spinner(
                "Analyzing URL..."
            ):

                try:

                    url_score, url_signals = (
                        analyze_url(url)
                    )

                    if url_score >= 70:

                        url_risk_level = "HIGH"

                    elif url_score >= 40:

                        url_risk_level = "MEDIUM"

                    else:

                        url_risk_level = "LOW"

                    st.divider()

                    st.subheader(
                        "URL Security Analysis"
                    )

                    show_risk_result(
                        url_score,
                        url_risk_level,
                        "URL Risk Score",
                    )

                    show_signals(
                        url_signals,
                        "Detected URL Signals",
                    )

                    show_recommendation(
                        url_risk_level
                    )

                except Exception as e:

                    st.error(
                        "URL analysis could not be completed. "
                        "Please check the URL and try again."
                    )

                    st.caption(
                        f"Technical detail: {e}"
                    )


# =========================================================
# SCREENSHOT ANALYSIS
# =========================================================

with screenshot_tab:

    st.subheader(
        "Screenshot Threat Scanner"
    )

    st.write(
        "Upload a screenshot of a suspicious SMS, WhatsApp message, "
        "email, or similar content. ScamShield extracts the text and analyzes it."
    )

    uploaded_image = st.file_uploader(
        "Upload suspicious screenshot",
        type=[
            "png",
            "jpg",
            "jpeg",
        ],
    )

    if uploaded_image is not None:

        try:

            image = Image.open(
                uploaded_image
            )

            image_col, details_col = (
                st.columns([1, 1])
            )

            with image_col:

                st.image(
                    image,
                    caption="Uploaded Screenshot",
                    width="stretch",
                )

            with details_col:

                st.markdown(
                    """
<div class="info-card">

<div class="info-title">
SCREENSHOT ANALYSIS PIPELINE
</div>

<div class="info-text">
Image → OCR → Threat Signals → AI Analysis → Risk Score
</div>

</div>
""",
                    unsafe_allow_html=True,
                )

                st.write("")

                if st.button(
                    "Analyze Screenshot",
                    type="primary",
                    width="stretch",
                ):

                    with st.spinner(
                        "Reading screenshot..."
                    ):

                        extracted_text = (
                            extract_text_from_image(
                                image
                            )
                        )

                    if (
                        not extracted_text
                        or not extracted_text.strip()
                    ):

                        st.warning(
                            "No readable text was detected "
                            "in the screenshot."
                        )

                    else:

                        st.markdown(
                            "### Extracted Text"
                        )

                        st.text_area(
                            "Text detected from screenshot",
                            extracted_text,
                            height=150,
                            disabled=True,
                        )

                        (
                            screenshot_rule_score,
                            screenshot_signals,
                        ) = detect_signals(
                            extracted_text
                        )

                        with st.spinner(
                            "Analyzing screenshot content..."
                        ):

                            screenshot_ai_analysis = (
                                analyze_with_ai(
                                    extracted_text
                                )
                            )

                        (
                            screenshot_score,
                            screenshot_risk_level,
                        ) = calculate_risk(
                            screenshot_rule_score,
                            screenshot_ai_analysis,
                        )

                        st.divider()

                        st.subheader(
                            "Screenshot Security Analysis"
                        )

                        show_risk_result(
                            screenshot_score,
                            screenshot_risk_level,
                        )

                        st.markdown(
                            "### AI Security Analysis"
                        )

                        st.info(
                            screenshot_ai_analysis
                        )

                        show_signals(
                            screenshot_signals
                        )

                        show_recommendation(
                            screenshot_risk_level
                        )

        except Exception:

            st.error(
                "The screenshot could not be processed. "
                "Please upload a valid PNG or JPG image."
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div class="footer">

SCAMSHIELD • AI-POWERED SCAM RISK ASSESSMENT

<br>

Always verify suspicious requests through official channels.

</div>
""",
    unsafe_allow_html=True,
)