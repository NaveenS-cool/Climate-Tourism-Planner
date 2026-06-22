import streamlit as st
from datetime import datetime
from services.api.locator import get_coords
from services.api.climate import get_climate, hist_climate
from services.api.destination import get_terrain_type
from services.scores import compute_tci, z_score


def show_dashboard():
    destination = st.session_state["destination"]

    st.markdown("""
    <style>
    /* Reset & Base */
    #root > div:first-child { background: transparent !important; }
    .stApp { background: transparent !important; }
    [data-testid="stHeader"] { display: none; }
    [data-testid="stMainBlockContainer"],
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        min-height: 100vh !important;
        padding: 2.5rem 1.5rem 3rem !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    [data-testid="stMainBlockContainer"] > div:first-child,
    .block-container > div:first-child {
        width: 100% !important;
    }

    /* Ambient Background */
    .earth-bg {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        background: linear-gradient(160deg,
            #0d2b1e 0%,
            #1a3d2b 30%,
            #1f4d38 55%,
            #162e23 80%,
            #0b1f17 100%
        );
    }

    /* Subtle noise texture overlay */
    .earth-bg::after {
        content: '';
        position: absolute;
        inset: 0;
        background-image:
            radial-gradient(ellipse 80% 60% at 20% 30%, rgba(64,145,108,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 80% at 75% 70%, rgba(82,121,111,0.14) 0%, transparent 55%),
            radial-gradient(ellipse 50% 40% at 50% 10%, rgba(149,213,178,0.07) 0%, transparent 60%);
        animation: ambientDrift 20s ease-in-out infinite alternate;
    }

    @keyframes ambientDrift {
        0%   { opacity: 0.7; transform: scale(1); }
        100% { opacity: 1;   transform: scale(1.04); }
    }

    .leaf {
        position: absolute;
        opacity: 0;
        background: #52b788;
        border-radius: 0 50% 50% 50%;
        animation: leafFloat linear infinite;
        pointer-events: none;
    }

    @keyframes leafFloat {
        0%   { transform: translateY(110vh) rotate(0deg) scale(1);   opacity: 0; }
        8%   { opacity: 0.12; }
        92%  { opacity: 0.12; }
        100% { transform: translateY(-10vh) rotate(540deg) scale(0.5); opacity: 0; }
    }

    /* Page Header */
    .dash-header {
        text-align: center;
        margin-bottom: 2.8rem;
        position: relative;
        z-index: 1;
    }

    .dash-eyebrow {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 0.72rem;
        font-weight: 400;
        letter-spacing: 0.18em;
        color: #52b788;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .dashboard-title {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-weight: 200;
        font-size: 3.6rem;
        letter-spacing: -0.03em;
        line-height: 1;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .dashboard-title strong {
        font-weight: 700;
        color: #a3e4c0;
    }

    .terrain-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(82,183,136,0.12);
        border: 1px solid rgba(82,183,136,0.25);
        border-radius: 100px;
        padding: 0.3rem 0.85rem;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.78rem;
        font-weight: 500;
        color: rgba(255,255,255,0.75);
        letter-spacing: 0.04em;
        margin-top: 0.4rem;
    }

    .terrain-badge::before {
        content: '◈';
        color: #52b788;
        font-size: 0.7rem;
    }

    /* Climate Score Panel */
    .score-panel {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 24px;
        padding: 2rem 2rem 1.5rem;
        margin-bottom: 1.6rem;
        position: relative;
        z-index: 1;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }

    .panel-eyebrow {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 0.68rem;
        font-weight: 400;
        letter-spacing: 0.18em;
        color: rgba(82,183,136,0.7);
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 0.8rem;
    }

    /* Gauge SVG styling */
    .gauge-wrap {
        display: flex;
        justify-content: center;
        position: relative;
        z-index: 1;
        margin: 0 auto;
    }

    .gauge-track {
        fill: none;
        stroke: rgba(255,255,255,0.07);
        stroke-width: 8;
        stroke-linecap: round;
    }

    .gauge-glow {
        fill: none;
        stroke: url(#gaugeGlow);
        stroke-width: 12;
        stroke-linecap: round;
        opacity: 0.25;
        filter: blur(4px);
    }

    .gauge-fill {
        fill: none;
        stroke: url(#gaugeGrad);
        stroke-width: 8;
        stroke-linecap: round;
        transition: stroke-dashoffset 1.2s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .gauge-score-num {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 3.8rem;
        font-weight: 700;
        fill: #ffffff;
        text-anchor: middle;
        dominant-baseline: central;
    }

    .gauge-score-label {
        font-family: 'SF Mono', 'Fira Code', monospace;
        font-size: 0.6rem;
        fill: rgba(255,255,255,0.35);
        text-anchor: middle;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .gauge-score-quality {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        text-anchor: middle;
        letter-spacing: 0.06em;
    }

    /* Min / Max arc markers */
    .gauge-tick {
        fill: rgba(255,255,255,0.2);
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.58rem;
        text-anchor: middle;
    }

    /* Date Slider */
    .slider-wrap {
        position: relative;
        z-index: 1;
        margin-bottom: 2rem;
    }

    /* Container */
    div[data-testid="stSlider"] > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.6rem 0.8rem !important;
    }

    /* Label */
    div[data-testid="stSlider"] label {
        color: rgba(255,255,255,0.35) !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
    }

    /* Track */
    [data-baseweb="slider"] [data-testid="stSliderTrack"],
    [data-baseweb="slider"] > div > div:first-child {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 100px !important;
        height: 3px !important;
    }

    /* Filled portion */
    [data-baseweb="slider"] [data-testid="stSliderTrackFill"] {
        background: linear-gradient(90deg, #1a5c3a, #52b788) !important;
        border-radius: 100px !important;
    }

    /* Thumb */
    [data-baseweb="slider"] [role="slider"] {
        background: #ffffff !important;
        box-shadow:
            0 0 0 3px rgba(82,183,136,0.5),
            0 4px 16px rgba(0,0,0,0.35) !important;
        border: none !important;
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        cursor: grab !important;
        transition: box-shadow 0.25s ease !important;
    }

    [data-baseweb="slider"] [role="slider"]:hover {
        box-shadow:
            0 0 0 6px rgba(82,183,136,0.25),
            0 6px 20px rgba(0,0,0,0.4) !important;
    }

    [data-baseweb="slider"] [role="slider"]:active {
        cursor: grabbing !important;
        box-shadow:
            0 0 0 4px rgba(82,183,136,0.4),
            0 2px 8px rgba(0,0,0,0.3) !important;
    }

    /* Tick labels */
    [data-testid="stTickBar"] {
        margin-top: 0.4rem !important;
    }

    [data-testid="stTickBar"] p {
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        font-size: 0.62rem !important;
        color: rgba(255,255,255,0.3) !important;
    }

    /* Timeline Scale Banner */
    .timeline-banner {
        display: flex;
        width: calc(100% - 3.2rem);
        margin: 1.5rem 1.6rem 0.5rem 1.6rem;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        overflow: hidden;
        position: relative;
        z-index: 1;
    }
    .timeline-region {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.4rem 0.2rem;
        text-align: center;
    }
    .timeline-region.past {
        background: rgba(255, 255, 255, 0.01);
        color: rgba(255, 255, 255, 0.35);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .timeline-region.current {
        background: rgba(82, 183, 136, 0.1);
        color: #52b788;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    .timeline-region.future {
        background: rgba(255, 255, 255, 0.03);
        color: rgba(255, 255, 255, 0.6);
    }
    .timeline-icon {
        font-size: 0.72rem;
        margin-right: 0.3rem;
    }

    /* Metric Row */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        position: relative;
        z-index: 1;
        margin-bottom: 0.8rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 18px;
        padding: 1.4rem 1rem 1.2rem;
        text-align: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 4px 24px rgba(0,0,0,0.18);
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.28);
    }

    .metric-icon {
        font-size: 1.1rem;
        margin-bottom: 0.45rem;
        display: block;
        opacity: 0.55;
    }

    .metric-label {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #111827;
        line-height: 1;
    }

    .metric-unit {
        font-size: 0.9rem;
        font-weight: 400;
        color: #6b7280;
        margin-left: 0.05rem;
    }

    /* Z-Score Row */
    .zscores-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        position: relative;
        z-index: 1;
        margin-bottom: 2rem;
    }

    .zscore-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .zscore-card:hover {
        transform: translateY(-3px);
        border-color: rgba(82,183,136,0.2);
    }

    .zscore-label {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.65rem;
        font-weight: 400;
        color: rgba(255,255,255,0.35);
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }

    .zscore-value {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 1.65rem;
        font-weight: 700;
        line-height: 1;
    }

    .zscore-sigma {
        font-size: 0.9rem;
        font-weight: 400;
        opacity: 0.6;
    }

    .zscore-positive { color: #4ade80; }
    .zscore-negative { color: #f87171; }

    /* Section Dividers */
    .section-sep {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin: 1.6rem 0 1rem;
        position: relative;
        z-index: 1;
    }

    .section-sep-line {
        flex: 1;
        height: 1px;
        background: rgba(255,255,255,0.06);
    }

    .section-sep-label {
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 0.65rem;
        font-weight: 400;
        letter-spacing: 0.14em;
        color: rgba(255,255,255,0.28);
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* Back Button */
    .back-btn-wrapper {
        position: relative;
        z-index: 1;
        text-align: center;
        margin-top: 1rem;
    }

    div[data-testid="stButton"] > button {
        background: transparent !important;
        color: rgba(255,255,255,0.45) !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        font-weight: 400 !important;
        font-size: 0.82rem !important;
        padding: 0.45rem 1.4rem !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 100px !important;
        letter-spacing: 0.04em !important;
        transition: all 0.25s ease !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }

    div[data-testid="stButton"] > button:hover {
        border-color: rgba(82,183,136,0.4) !important;
        color: rgba(255,255,255,0.75) !important;
        background: rgba(82,183,136,0.08) !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Responsive */
    @media (max-width: 600px) {
        .dashboard-title { font-size: 2.4rem; }
        .metrics-row, .zscores-row { grid-template-columns: 1fr; }
        .metric-value { font-size: 1.6rem; }
        .zscore-value { font-size: 1.4rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    leaves = [
        {"left": "5%",  "size": "22px", "dur": "20s", "delay": "0s"},
        {"left": "18%", "size": "30px", "dur": "25s", "delay": "4s"},
        {"left": "60%", "size": "18px", "dur": "22s", "delay": "1.5s"},
        {"left": "80%", "size": "34px", "dur": "28s", "delay": "7s"},
        {"left": "93%", "size": "24px", "dur": "21s", "delay": "3s"},
    ]
    leaf_divs = "".join(
        f'<div class="leaf" style="left:{l["left"]};width:{l["size"]};height:{l["size"]};'
        f'animation-duration:{l["dur"]};animation-delay:{l["delay"]};"></div>'
        for l in leaves
    )
    st.markdown(f'<div class="earth-bg">{leaf_divs}</div>', unsafe_allow_html=True)

    # Loader
    loader_placeholder = st.empty()
    loader_html = """
    <style>
    .dash-loader-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 5rem 0;
        position: relative;
        z-index: 1;
        gap: 1.2rem;
    }
    .dash-loader-ring {
        width: 44px;
        height: 44px;
        border: 2px solid rgba(255,255,255,0.06);
        border-top-color: #52b788;
        border-radius: 50%;
        animation: dashLoaderSpin 0.9s linear infinite;
    }
    @keyframes dashLoaderSpin { to { transform: rotate(360deg); } }
    .dash-loader-text {
        color: rgba(255,255,255,0.5);
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        font-size: 0.92rem;
        font-weight: 300;
        letter-spacing: 0.03em;
    }
    </style>
    <div class="dash-loader-wrap">
        <div class="dash-loader-ring"></div>
        <div class="dash-loader-text">Reading climate data for {dest}</div>
    </div>
    """.replace("{dest}", destination)
    loader_placeholder.markdown(loader_html, unsafe_allow_html=True)

    # Backend calls (untouched)
    lat, lon = get_coords(destination)
    raw_daily, _ = get_climate(lat, lon)
    terrain_data = get_terrain_type(lat, lon)
    hist_data = hist_climate(lat, lon)

    current = {
        "dates":    raw_daily["time"],
        "temp":     raw_daily["temperature_2m_mean"],
        "humidity": raw_daily["relative_humidity_2m_mean"],
        "precip":   raw_daily["precipitation_sum"],
    }

    tci_scores = []
    for i in range(len(current["dates"])):
        sunshine = raw_daily.get("sunshine_duration", [0] * len(current["dates"]))[i]
        sunshine_hours = (sunshine / 3600) if sunshine else 0
        tci = compute_tci(
            tmax=raw_daily["temperature_2m_max"][i],
            tmean=raw_daily["temperature_2m_mean"][i],
            rhmin=raw_daily["relative_humidity_2m_min"][i],
            rhmean=raw_daily["relative_humidity_2m_mean"][i],
            rain_mm=raw_daily["precipitation_sum"][i],
            sunshine_hours=sunshine_hours,
            wind_kmh=raw_daily["wind_speed_10m_max"][i],
        )
        tci_scores.append(tci)

    terrain_type = terrain_data["primary"]

    loader_placeholder.empty()

    # Page Header
    st.markdown(
        f"""
        <div class="dash-header">
            <div class="dash-eyebrow">Climate Planner</div>
            <div class="dashboard-title"><strong>{destination}</strong></div>
            <div class="terrain-badge">{terrain_type.title()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Climate Score Gauge Placeholder
    gauge_placeholder = st.empty()

    # Date Slider
    today_str = datetime.today().strftime("%Y-%m-%d")
    total_days = len(current["dates"])
    
    # Calculate counts and percentages dynamically
    past_count = sum(1 for d in current["dates"] if d < today_str)
    current_count = sum(1 for d in current["dates"] if d == today_str)
    future_count = sum(1 for d in current["dates"] if d > today_str)
    
    # Avoid division by zero just in case
    safe_total = total_days if total_days > 0 else 1
    past_pct = (past_count / safe_total) * 100
    current_pct = (current_count / safe_total) * 100
    future_pct = (future_count / safe_total) * 100

    # Render visual region scale banner
    timeline_banner_html = f"""
    <div class="timeline-banner">
        <div class="timeline-region past" style="width: {past_pct:.1f}%;">
            <span class="timeline-icon">⏮</span>Past ({past_count}d)
        </div>
        <div class="timeline-region current" style="width: {current_pct:.1f}%;">
            <span class="timeline-icon">🟢</span>Today
        </div>
        <div class="timeline-region future" style="width: {future_pct:.1f}%;">
            Forecast ({future_count}d)<span class="timeline-icon">⏭</span>
        </div>
    </div>
    """
    st.markdown(timeline_banner_html, unsafe_allow_html=True)

    date_labels = []
    for idx, d in enumerate(current["dates"]):
        dt = datetime.strptime(d, "%Y-%m-%d")
        lbl = dt.strftime("%d %b")
        if d == today_str:
            lbl += " (Today)"
        elif idx == 0:
            lbl += " (Past)"
        elif idx == total_days - 1:
            lbl += " (Forecast)"
        date_labels.append(lbl)

    # Use past_count as default index (which maps to today if present)
    default_idx = past_count if 0 <= past_count < total_days else total_days // 2

    selected_date = st.select_slider(
        "SELECT DATE",
        options=date_labels,
        value=date_labels[default_idx],
        key="date_slider",
        label_visibility="collapsed",
    )
    selected_idx  = date_labels.index(selected_date)
    selected_tci  = tci_scores[selected_idx]

    # Climate Score Gauge
    # Score quality label
    if selected_tci >= 80:
        quality, quality_color = "Excellent",  "#4ade80"
    elif selected_tci >= 65:
        quality, quality_color = "Good",       "#a3e4c0"
    elif selected_tci >= 50:
        quality, quality_color = "Fair",       "#fbbf24"
    elif selected_tci >= 35:
        quality, quality_color = "Poor",       "#f97316"
    else:
        quality, quality_color = "Harsh",      "#f87171"

    arc_length    = 257.6
    target_offset = arc_length * (1 - selected_tci / 100)
    anim_key      = f"gs{selected_idx}"

    # Gradient colours keyed to score (bright against dark bg)
    if selected_tci >= 70:
        grad_start, grad_end = "#00ffa3", "#00c97a"   # vivid mint → emerald
    elif selected_tci >= 50:
        grad_start, grad_end = "#f9cb45", "#f97316"   # amber → orange
    else:
        grad_start, grad_end = "#ff6b6b", "#c0392b"   # coral → red

    gauge_html = f"""
    <style>
    .gauge-fill {{
        fill: none;
        stroke: url(#gaugeGrad);
        stroke-width: 8;
        stroke-linecap: round;
        stroke-dasharray: {arc_length};
        stroke-dashoffset: {arc_length};
        animation: {anim_key} 1.4s cubic-bezier(0.23,1,0.32,1) forwards;
    }}
    .gauge-glow {{
        fill: none;
        stroke: url(#gaugeGlow);
        stroke-width: 14;
        stroke-linecap: round;
        stroke-dasharray: {arc_length};
        stroke-dashoffset: {arc_length};
        opacity: 0.22;
        filter: blur(5px);
        animation: {anim_key} 1.4s cubic-bezier(0.23,1,0.32,1) forwards;
    }}
    @keyframes {anim_key} {{
        from {{ stroke-dashoffset: {arc_length}; }}
        to   {{ stroke-dashoffset: {target_offset}; }}
    }}
    .gauge-score-num {{
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 42px;
        font-weight: 700;
        fill: #ffffff;
        text-anchor: middle;
        dominant-baseline: central;
        opacity: 0;
        animation: numFadeIn 0.6s ease-out 1s forwards;
    }}
    .gauge-score-quality {{
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 11px;
        font-weight: 600;
        fill: {quality_color};
        text-anchor: middle;
        dominant-baseline: central;
        letter-spacing: 0.08em;
        opacity: 0;
        animation: numFadeIn 0.6s ease-out 1.2s forwards;
    }}
    .gauge-score-sublabel {{
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 8px;
        fill: rgba(255,255,255,0.25);
        text-anchor: middle;
        dominant-baseline: central;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0;
        animation: numFadeIn 0.6s ease-out 1.3s forwards;
    }}
    @keyframes numFadeIn {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    <div class="score-panel">
        <div class="panel-eyebrow">Climate Comfort Index</div>
        <div class="gauge-wrap">
            <svg viewBox="0 0 220 145" width="100%" height="auto" style="max-width:340px;">
                <defs>
                    <!-- Vivid contrasting gradient, always visible on dark bg -->
                    <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%"   stop-color="{grad_start}" />
                        <stop offset="100%" stop-color="{grad_end}" />
                    </linearGradient>
                    <!-- Glow layer same colours but wider/blurred -->
                    <linearGradient id="gaugeGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%"   stop-color="{grad_start}" />
                        <stop offset="100%" stop-color="{grad_end}" />
                    </linearGradient>
                </defs>
                <!-- Track -->
                <path class="gauge-track"
                      d="M 28 118 A 82 82 0 0 1 192 118"
                      fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8" stroke-linecap="round"/>
                <!-- Glow layer -->
                <path class="gauge-glow"
                      d="M 28 118 A 82 82 0 0 1 192 118"/>
                <!-- Fill layer -->
                <path class="gauge-fill"
                      d="M 28 118 A 82 82 0 0 1 192 118"/>
                <!-- Endpoint dots -->
                <circle cx="28"  cy="118" r="3" fill="rgba(255,255,255,0.12)"/>
                <circle cx="192" cy="118" r="3" fill="rgba(255,255,255,0.12)"/>
                <!-- Tick labels -->
                <text x="22"  y="134" class="gauge-tick" fill="rgba(255,255,255,0.18)"
                      font-size="7" text-anchor="middle">0</text>
                <text x="199" y="134" class="gauge-tick" fill="rgba(255,255,255,0.18)"
                      font-size="7" text-anchor="middle">100</text>
                <!-- Score number -->
                <text class="gauge-score-num"  x="110" y="78">{selected_tci:.0f}</text>
                <!-- Quality label -->
                <text class="gauge-score-quality" x="110" y="108">{quality}</text>
                <!-- Sub-label -->
                <text class="gauge-score-sublabel" x="110" y="126">TCI Score</text>
            </svg>
        </div>
    </div>
    """
    gauge_placeholder.markdown(gauge_html, unsafe_allow_html=True)

    # Current Conditions
    st.markdown(
        '<div class="section-sep"><div class="section-sep-line"></div>'
        '<div class="section-sep-label">Current Conditions</div>'
        '<div class="section-sep-line"></div></div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Temperature</div>
                <div class="metric-value">{current["temp"][selected_idx]:.1f}<span class="metric-unit">°C</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Humidity</div>
                <div class="metric-value">{current["humidity"][selected_idx]:.1f}<span class="metric-unit">%</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Precipitation</div>
                <div class="metric-value">{current["precip"][selected_idx]:.1f}<span class="metric-unit">mm</span></div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Historical Z-Scores
    st.markdown(
        '<div class="section-sep"><div class="section-sep-line"></div>'
        '<div class="section-sep-label">Z SCORES</div>'
        '<div class="section-sep-line"></div></div>',
        unsafe_allow_html=True,
    )

    z_temp   = z_score(current["temp"][selected_idx],     hist_data["temp_mean"],          hist_data["temp_std"])
    z_rh     = z_score(current["humidity"][selected_idx], hist_data["rh_mean"],             hist_data["rh_std"])
    z_precip = z_score(current["precip"][selected_idx],   hist_data["precipitation_mean"],  hist_data["precipitation_std"])

    zcol1, zcol2, zcol3 = st.columns(3)
    with zcol1:
        zcls = "zscore-positive" if z_temp >= 0 else "zscore-negative"
        st.markdown(
            f"""<div class="zscore-card">
                <div class="zscore-label">Temperature</div>
                <div class="zscore-value {zcls}">{z_temp:+.2f}<span class="zscore-sigma"> σ</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with zcol2:
        zcls = "zscore-positive" if z_rh >= 0 else "zscore-negative"
        st.markdown(
            f"""<div class="zscore-card">
                <div class="zscore-label">Humidity</div>
                <div class="zscore-value {zcls}">{z_rh:+.2f}<span class="zscore-sigma"> σ</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with zcol3:
        zcls = "zscore-positive" if z_precip >= 0 else "zscore-negative"
        st.markdown(
            f"""<div class="zscore-card">
                <div class="zscore-label">Precipitation</div>
                <div class="zscore-value {zcls}">{z_precip:+.2f}<span class="zscore-sigma"> σ</span></div>
            </div>""",
            unsafe_allow_html=True,
        )

    # Back Button
    st.markdown('<div class="back-btn-wrapper">', unsafe_allow_html=True)
    if st.button("← Back"):
        st.session_state["current_page"] = "intro"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
