import streamlit as st
import time


def show_intro():
    """Renders the introductory landing page with animated background and destination input."""

    
    # CUSTOM CSS — Earthy & Green animated background
    
    #  - .earth-bg: full-screen gradient that slowly shifts hues
    #  - .leaf: procedurally-placed leaf emblems that drift upward
    #  - .orb: soft glowing circles in warm earth tones
    #  - div[data-testid="column"]:nth-of-type(2): glass-morphism card on middle col
    #  - .stTextInput / .stButton overrides for premium look
    
    st.html(
        """
        <style>
        /* ---------- RESET / BASE ---------- */
        #root > div:first-child {
            background: transparent !important;
        }
        .stApp {
            background: transparent !important;
        }
        /* Streamlit header (hamburger menu bar) — hide so it doesn't offset 100vh */
        [data-testid="stHeader"] {
            display: none;
        }

        /* 1. Target the absolute main container in modern Streamlit */
        [data-testid="stMainBlockContainer"], .block-container {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            min-height: 100vh !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }

        /* 2. Target the inner wrapper Streamlit injects and force it to the middle */
        [data-testid="stMainBlockContainer"] > div:first-child,
        .block-container > div:first-child {
            margin-top: auto !important;
            margin-bottom: auto !important;
            width: 100% !important;
        }

        /* ---------- ANIMATED BACKGROUND ---------- */
        .earth-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;

            /* Shifting gradient between earthy greens and warm browns */
            background: linear-gradient(
                135deg,
                #1b4332 0%,
                #2d6a4f 25%,
                #40916c 50%,
                #52796f 75%,
                #354f52 100%
            );
            background-size: 400% 400%;
            animation: gradientShift 16s ease-in-out infinite;
        }

        @keyframes gradientShift {
            0%   { background-position: 0% 50%; }
            25%  { background-position: 50% 0%; }
            50%  { background-position: 100% 50%; }
            75%  { background-position: 50% 100%; }
            100% { background-position: 0% 50%; }
        }

        /* ---------- FLOATING LEAVES ---------- */
        .leaf {
            position: absolute;
            width: 28px;
            height: 28px;
            opacity: 0.15;
            background: #52b788;
            border-radius: 0 50% 50% 50%;
            animation: leafFloat linear infinite;
            pointer-events: none;
        }

        /* Each leaf gets its position, size, and timing via inline styles */
        @keyframes leafFloat {
            0%   { transform: translateY(110vh) rotate(0deg) scale(1); opacity: 0; }
            10%  { opacity: 0.18; }
            90%  { opacity: 0.18; }
            100% { transform: translateY(-10vh) rotate(720deg) scale(0.6); opacity: 0; }
        }

        /* ---------- GLOWING EARTH ORBS ---------- */
        .orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            pointer-events: none;
            animation: orbPulse 8s ease-in-out infinite alternate;
        }

        @keyframes orbPulse {
            0%   { transform: scale(1); opacity: 0.25; }
            100% { transform: scale(1.3); opacity: 0.45; }
        }

        /* ---------- GLASS CARD — applied to the middle column ---------- */
        div[data-testid="column"]:nth-of-type(2) > div {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(16px) saturate(150%);
            -webkit-backdrop-filter: blur(16px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 32px;
            padding: 3rem 3.5rem !important;
            text-align: center;
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
            transition: box-shadow 0.4s ease;
        }

        div[data-testid="column"]:nth-of-type(2) > div:hover {
            box-shadow: 0 28px 96px rgba(0, 0, 0, 0.5);
        }

        /* ---------- HEADLINE ---------- */
        .headline {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-weight: 700;
            font-size: 2.6rem;
            letter-spacing: -0.02em;
            color: #fff;
            margin-bottom: 0.4rem;
            line-height: 1.2;
        }

        .headline span {
            color: #95d5b2;
        }

        .subhead {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-weight: 300;
            font-size: 1.05rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 2.2rem;
        }

        /* ---------- STREAMLIT OVERRIDES (Text Input) ---------- */
        div[data-testid="stTextInput"] {
            margin-bottom: 1.2rem;
        }

        div[data-testid="stTextInput"] > div {
            background: rgba(255, 255, 255, 0.10) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.20) !important;
            border-radius: 14px !important;
            transition: all 0.3s ease !important;
        }

        div[data-testid="stTextInput"] > div:focus-within {
            border-color: #95d5b2 !important;
            box-shadow: 0 0 0 3px rgba(149, 213, 178, 0.25) !important;
            background: rgba(255, 255, 255, 0.16) !important;
        }

        div[data-testid="stTextInput"] input {
            color: #fff !important;
            font-size: 1.05rem !important;
            padding: 0.8rem 1rem !important;
            caret-color: #95d5b2 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: rgba(255, 255, 255, 0.45) !important;
        }

        /* ---------- STREAMLIT OVERRIDES (Button) ---------- */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }

        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #40916c, #2d6a4f) !important;
            color: #fff !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 0.65rem 2.8rem !important;
            border: none !important;
            border-radius: 40px !important;
            letter-spacing: 0.01em;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 24px rgba(45, 106, 79, 0.35) !important;
            cursor: pointer;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-3px) scale(1.02) !important;
            box-shadow: 0 12px 36px rgba(45, 106, 79, 0.5) !important;
            background: linear-gradient(135deg, #52b788, #2d6a4f) !important;
        }

        div[data-testid="stButton"] > button:active {
            transform: translateY(0) scale(0.98) !important;
            box-shadow: 0 4px 12px rgba(45, 106, 79, 0.3) !important;
        }

        /* ---------- RESPONSIVE ---------- */
        @media (max-width: 600px) {
            .headline   { font-size: 1.8rem; }
        }
        </style>
        """
    )

    
    # ANIMATED BACKGROUND MARKUP
    
    #  - 5 leaves with varying sizes, speeds, and horizontal positions
    #  - 3 orbs in warm earth tones (amber, terracotta, olive)
    
    leaves = [
        {"left": "8%",  "size": "24px",  "dur": "18s",  "delay": "0s"},
        {"left": "22%", "size": "32px",  "dur": "22s",  "delay": "3s"},
        {"left": "55%", "size": "20px",  "dur": "20s",  "delay": "1s"},
        {"left": "78%", "size": "36px",  "dur": "26s",  "delay": "6s"},
        {"left": "92%", "size": "26px",  "dur": "19s",  "delay": "4s"},
    ]
    leaf_divs = "".join(
        f'<div class="leaf" style="left:{l["left"]};width:{l["size"]};height:{l["size"]};'
        f'animation-duration:{l["dur"]};animation-delay:{l["delay"]};"></div>'
        for l in leaves
    )

    orbs = [
        {"left": "10%", "top": "15%",  "w": "320px", "h": "320px", "bg": "#d4a373", "dur": "10s"},
        {"left": "70%", "top": "60%",  "w": "400px", "h": "400px", "bg": "#e76f51", "dur": "12s"},
        {"left": "40%", "top": "70%",  "w": "280px", "h": "280px", "bg": "#a3b18a", "dur": "9s"},
    ]
    orb_divs = "".join(
        f'<div class="orb" style="left:{o["left"]};top:{o["top"]};width:{o["w"]};height:{o["h"]};'
        f'background:{o["bg"]};animation-duration:{o["dur"]};"></div>'
        for o in orbs
    )

    st.html(
        f'<div class="earth-bg">{leaf_divs}{orb_divs}</div>'
    )

    
    # MAIN CONTENT — centered in a narrow column using Streamlit columns
    
    # Columns [left_gutter, middle_content, right_gutter]
    # Ratio 1:1.5:1 keeps the card narrow on wide screens.
    
    def navigate_to_dashboard():
        dest = st.session_state.get("intro_dest", "").strip()
        if dest:
            st.session_state["destination"] = dest
            st.session_state["current_page"] = "dashboard"
            st.stop()

    _, col_content, _ = st.columns([1, 1.5, 1])

    with col_content:
        st.markdown(
            '<div class="headline">Climate<br><span>Tourism Planner</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="subhead">Discover your ideal travel window — powered by climate data</div>',
            unsafe_allow_html=True,
        )

        # --- Destination input ---
        destination = st.text_input(
            label="Destination",
            placeholder="e.g. Munnar, Kerala",
            label_visibility="collapsed",
            key="intro_dest",
        )

        # --- Submit button ---
        st.button(
            "🌿  Start Planning",
            type="primary",
            use_container_width=False,
            on_click=navigate_to_dashboard,
        )

