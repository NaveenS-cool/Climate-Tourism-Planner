import streamlit as st
from api.locator import get_coords
from api.climate import get_climate
from api.destination import get_terrain_type


def show_dashboard():
    destination = st.session_state["destination"]

    st.markdown(
        """
        <style>
        #root > div:first-child {
            background: transparent !important;
        }
        .stApp {
            background: transparent !important;
        }
        [data-testid="stHeader"] {
            display: none;
        }
        [data-testid="stMainBlockContainer"], .block-container {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            min-height: 100vh !important;
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        .earth-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            overflow: hidden;
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

        @keyframes leafFloat {
            0%   { transform: translateY(110vh) rotate(0deg) scale(1); opacity: 0; }
            10%  { opacity: 0.18; }
            90%  { opacity: 0.18; }
            100% { transform: translateY(-10vh) rotate(720deg) scale(0.6); opacity: 0; }
        }

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

        .dashboard-title {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-weight: 700;
            font-size: 2.8rem;
            letter-spacing: -0.02em;
            color: #ffffff;
            text-align: center;
            margin-bottom: 2.5rem;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        }

        .dashboard-title span {
            color: #95d5b2;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(14px) saturate(180%);
            -webkit-backdrop-filter: blur(14px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 20px;
            padding: 1.6rem 1rem;
            text-align: center;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            z-index: 1;
        }

        .metric-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 56px rgba(0, 0, 0, 0.35);
        }

        .metric-label {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            color: #4a5568;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
        }

        .metric-value {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #111827;
        }

        .back-btn-wrapper {
            position: relative;
            z-index: 1;
            margin-top: 2.5rem;
            text-align: center;
        }

        div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #40916c, #2d6a4f) !important;
            color: #fff !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.5rem 2rem !important;
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

        @media (max-width: 600px) {
            .dashboard-title { font-size: 1.8rem; }
            .metric-value { font-size: 1.6rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

    st.markdown(
        f'<div class="earth-bg">{leaf_divs}{orb_divs}</div>',
        unsafe_allow_html=True,
    )

    loader_placeholder = st.empty()

    loader_html = f"""
    <style>
    .dash-loader-wrap {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 0;
        position: relative;
        z-index: 1;
    }}
    .dash-loader-ring {{
        width: 52px;
        height: 52px;
        border: 4px solid rgba(255, 255, 255, 0.1);
        border-left-color: #95d5b2;
        border-right-color: #52b788;
        border-radius: 50%;
        animation: dashLoaderSpin 1s linear infinite;
    }}
    @keyframes dashLoaderSpin {{
        to {{ transform: rotate(360deg); }}
    }}
    .dash-loader-text {{
        margin-top: 1.5rem;
        color: rgba(255, 255, 255, 0.85);
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 1.05rem;
        font-weight: 300;
        letter-spacing: 0.03em;
    }}
    </style>
    <div class="dash-loader-wrap">
        <div class="dash-loader-ring"></div>
        <div class="dash-loader-text">Analyzing climate data for {destination}...</div>
    </div>
    """

    loader_placeholder.markdown(loader_html, unsafe_allow_html=True)

    lat, lon = get_coords(destination)
    climate_data = get_climate(lat, lon)
    terrain_data = get_terrain_type(lat, lon)

    loader_placeholder.empty()

    st.markdown(
        f'<div class="dashboard-title">🌍 <span>{destination}</span></div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value">{climate_data['temperature_2m']}°C</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Humidity</div>
                <div class="metric-value">{climate_data['relative_humidity_2m']}%</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Wind Speed</div>
                <div class="metric-value">{climate_data['wind_speed_10m']} Km/hr</div>
            </div>""",
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Type of Place</div>
                <div class="metric-value">{terrain_data['primary'].title()}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    if st.button("← Back to start"):
        st.session_state["current_page"] = "intro"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
