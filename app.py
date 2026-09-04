import streamlit as st
from analyzer import analyze_with_ai
from rules import detect_signals


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ScamShield | AI Threat Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 180, 255, 0.08), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(100, 70, 255, 0.08), transparent 30%),
            #070b12;
        color: #e8eef7;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* HEADER */

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 8px;
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #12395a, #0b1828);
        border: 1px solid rgba(0, 200, 255, 0.35);
        box-shadow: 0 0 25px rgba(0, 180, 255, 0.12);
        font-size: 28px;
    }

    .brand-name {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #f5f8fc;
    }

    .brand-tag {
        font-size: 13px;
        color: #7f93aa;
        margin-top: 2px;
    }

    .hero {
        margin-top: 35px;
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 42px;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #f5f8fc;
        margin-bottom: 12px;
    }

    .hero-title span {
        color: #4cc9ff;
    }

    .hero-subtitle {
        font-size: 16px;
        line-height: 1.6;
        color: #91a2b7;
        max-width: 720px;
    }

    /* INPUT */

    .section-label {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #7f93aa;
        margin-bottom: 8px;
    }

    div[data-testid="stTextArea"] textarea {
        background: #0a111b !important;
        color: #eaf1f8 !important;
        border: 1px solid #243447 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        padding: 16px !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border: 1px solid #28b8f2 !important;
        box-shadow: 0 0 0 1px rgba(40, 184, 242, 0.25) !important;
    }

    /* BUTTON */

    div.stButton > button {
        width: 100%;
        min-height: 52px;
        border-radius: 12px;
        border: 1px solid rgba(76, 201, 255, 0.45);
        background: linear-gradient(135deg, #0d6f9f, #1553a0);
        color: white;
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 0.5px;
        box-shadow: 0 10px 25px rgba(0, 100, 180, 0.2);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #65d5ff;
        transform: translateY(-1px);
        box-shadow: 0 14px 30px rgba(0, 150, 220, 0.25);
    }

    /* RESULTS */

    .result-header {
        margin-top: 42px;
        margin-bottom: 18px;
    }

    .result-title {
        font-size: 24px;
        font-weight: 800;
        color: #f5f8fc;
    }

    .result-subtitle {
        font-size: 13px;
        color: #71849a;
        margin-top: 3px;
    }

    .security-card {
        background: rgba(14, 22, 34, 0.92);
        border: 1px solid rgba(120, 150, 180, 0.16);
        border-radius: 18px;
        padding: 24px;
        min-height: 180px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.20);
    }

    .card-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        color: #71849a;
        margin-bottom: 12px;
    }

    .risk-score {
        font-size: 52px;
        line-height: 1;
        font-weight: 850;
        color: #f5f8fc;
    }

    .risk-score-small {
        font-size: 14px;
        color: #71849a;
        margin-left: 5px;
    }

    .risk-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.7px;
    }

    .risk-high {
        background: rgba(255, 70, 70, 0.12);
        border: 1px solid rgba(255, 80, 80, 0.35);
        color: #ff7b7b;
    }

    .risk-medium {
        background: rgba(255, 180, 50, 0.12);
        border: 1px solid rgba(255, 180, 50, 0.35);
        color: #ffc45c;
    }

    .risk-low {
        background: rgba(50, 210, 130, 0.12);
        border: 1px solid rgba(50, 210, 130, 0.35);
        color: #5de09a;
    }

    .signal {
        background: #0a111b;
        border: 1px solid #243447;
        border-radius: 10px;
        padding: 11px 13px;
        margin-bottom: 9px;
        color: #dce6f0;
        font-size: 14px;
    }

    .signal-icon {
        color: #ffbd4a;
        margin-right: 8px;
    }

    .no-signal {
        color: #7f93aa;
        font-size: 14px;
        padding-top: 8px;
    }

    .analysis-card,
    .recommendation {
        margin-top: 18px;
        background: rgba(14, 22, 34, 0.92);
        border: 1px solid rgba(120, 150, 180, 0.16);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.20);
    }

    .analysis-title,
    .recommendation-title {
        font-size: 18px;
        font-weight: 800;
        color: #f5f8fc;
        margin-bottom: 12px;
    }

    .analysis-description,
    .recommendation-text {
        color: #b7c7d8;
        line-height: 1.7;
        font-size: 14px;
    }

    .recommendation {
        background: linear-gradient(
            135deg,
            rgba(18, 55, 82, 0.65),
            rgba(13, 30, 50, 0.75)
        );
        border-color: rgba(76, 201, 255, 0.22);
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(120, 150, 180, 0.12);
        color: #5e7187;
        font-size: 12px;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px;
        }

        .brand-name {
            font-size: 25px;
        }

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div>
            <div class="brand-name">SCAMSHIELD</div>
            <div class="brand-tag">AI-POWERED DIGITAL THREAT DETECTION</div>
        </div>
    </div>

    <div class="hero">
        <div class="hero-title">
            Detect scams before they <span>cause damage.</span>
        </div>

        <div class="hero-subtitle">
            Analyze suspicious messages using rule-based threat detection
            and AI-powered security analysis. Identify warning signs,
            understand the risk, and know what to do next.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MESSAGE INPUT
# ============================================================

st.markdown(
    '<div class="section-label">Message Threat Scanner</div>',
    unsafe_allow_html=True,
)

message = st.text_area(
    "Suspicious message",
    placeholder=(
        "Paste the suspicious message here...\n\n"
        "Example: Your account will be blocked today. "
        "Click this link immediately to verify your identity."
    ),
    height=190,
    label_visibility="collapsed",
)

st.write("")

analyze_clicked = st.button(
    "🔍  SCAN FOR THREATS",
    type="primary",
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_clicked:

    if not message.strip():
        st.warning("⚠️ Please enter a suspicious message first.")

    else:
        with st.spinner("🧠 AI is analyzing the message..."):

            # Existing backend
            score, signals = detect_signals(message)
            ai_analysis = analyze_with_ai(message)

        # Risk level
        if score >= 70:
            risk_level = "HIGH RISK"
            risk_class = "risk-high"
            risk_icon = "🚨"

        elif score >= 40:
            risk_level = "MEDIUM RISK"
            risk_class = "risk-medium"
            risk_icon = "⚠️"

        else:
            risk_level = "LOW RISK"
            risk_class = "risk-low"
            risk_icon = "✓"

        # ----------------------------------------------------
        # RESULT HEADER
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="result-header">
                <div class="result-title">Security Analysis</div>
                <div class="result-subtitle">
                    Threat assessment generated from your submitted message
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        score_col, signals_col = st.columns([1, 2])

        with score_col:
            st.markdown(
                f"""
                <div class="security-card">
                    <div class="card-label">Threat Risk Score</div>

                    <div>
                        <span class="risk-score">{score}</span>
                        <span class="risk-score-small">/ 100</span>
                    </div>

                    <div class="risk-badge {risk_class}">
                        {risk_icon} &nbsp; {risk_level}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with signals_col:
            signal_html = """
            <div class="security-card">
                <div class="card-label">Detected Threat Signals</div>
            """

            if signals:
                for signal in signals:
                    signal_html += f"""
                    <div class="signal">
                        <span class="signal-icon">⚠</span>
                        {signal}
                    </div>
                    """
            else:
                signal_html += """
                <div class="no-signal">
                    ✓ No obvious scam signals were detected.
                </div>
                """

            signal_html += "</div>"

            st.markdown(
                signal_html,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="analysis-card">
                <div class="analysis-title">
                    🤖 AI Security Analysis
                </div>
                <div class="analysis-description">
                    {ai_analysis}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if score >= 70:
            recommendation = (
                "Do not click suspicious links or share sensitive information. "
                "Verify the request through the organization's official website "
                "or app."
            )
        elif score >= 40:
            recommendation = (
                "Be cautious. Verify the sender and request through an official "
                "channel before taking any action."
            )
        else:
            recommendation = (
                "No major risk signals were detected, but always verify "
                "unexpected requests before responding or sharing information."
            )

        st.markdown(
            f"""
            <div class="recommendation">
                <div class="recommendation-title">
                    🛡️ Recommended Action
                </div>
                <div class="recommendation-text">
                    {recommendation}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        SCAMSHIELD &nbsp;•&nbsp; AI-POWERED SCAM RISK ASSESSMENT
        <br>
        Always verify suspicious requests through official channels.
    </div>
    """,
    unsafe_allow_html=True,
)   