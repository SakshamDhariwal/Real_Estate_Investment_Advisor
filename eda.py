from fpdf import FPDF

def run(df):
    import streamlit as st
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.io as pio
    import base64
    import plotly.express as px
    import plotly.graph_objects as go
    from pathlib import Path

    # from theme import apply_global_theme, render_sidebar_brand
    # from components import render_navbar, render_hero

    # ======================================================
    # PAGE CONFIG
    # ======================================================
    # st.set_page_config(
    #     page_title="Real Estate EDA Premium",
    #     layout="wide",
    #     initial_sidebar_state="expanded"
    # )
    # apply_global_theme()

    pio.templates.default = "plotly_white"
    num_cols = [
        "Price_in_Lakhs","Size_in_SqFt","Price_per_SqFt","Year_Built",
        "Nearby_Schools","Nearby_Hospitals","Public_Transport_Accessibility",
        "Parking_Space","BHK"
    ]
    # ======================================================
    # LOAD DATA
    # ======================================================
    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR / "cleaned_data.csv"

    def get_base64(img):
        with open(img, "rb") as f:
            return base64.b64encode(f.read()).decode()

    img64 = get_base64(BASE_DIR / "assets/building.png")

    @st.cache_data
    def load_data():
        return pd.read_csv(DATA_PATH)

    # 🔥 USE SHARED DATA IF AVAILABLE
    if "shared_df" in st.session_state:
        df = st.session_state["shared_df"].copy()
    else:
        df = load_data()

    # ======================================================
    # CLEAN NUMERIC
    # ======================================================


    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Age_of_Property" not in df.columns:
        df["Age_of_Property"] = 2026 - df["Year_Built"]

    # ======================================================
    # PREMIUM CSS (same vibe as app.py)
    # ======================================================
    st.markdown(f"""
    <style>

    html, body, [class*="css"] {{
        font-family: Inter, Arial, sans-serif;
    }}

    .stApp {{
        background:#eef3f4;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        min-width:320px !important;
        max-width:320px !important;
        border-right:1px solid rgba(255,255,255,0.06);
    }}

    section[data-testid="stSidebar"] > div:first-child {{
        background:
        linear-gradient(
            rgba(5,8,35,0.22),
            rgba(5,8,35,0.45)
        ),
        url("data:image/png;base64,{img64}");
        background-size:cover !important;
        background-position:center top !important;
        background-repeat:no-repeat !important;
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top:1rem;
        background:transparent !important;
    }}

    section[data-testid="stSidebar"] * {{
        color:white !important;
    }}

    /* glass controls */
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSlider {{
        background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:16px;
        padding:8px;
        backdrop-filter:blur(8px);
        margin-bottom:10px;
    }}

    /* MAIN */
    .block-container {{
        padding-top:1.2rem;
        padding-left:1.5rem;
        padding-right:1.5rem;
        padding-bottom:2rem;
        max-width:1600px;
    }}

    .hero {{
            background: linear-gradient(135deg, #0f766e 0%, #164e63 50%, #1d4ed8 100%);
            color: white;
            border-radius: 26px;
            padding: 30px 32px;
            margin-bottom: 18px;
            box-shadow: 0 18px 40px rgba(15, 118, 110, 0.18);
            margin-top: -20px;
        }}

    .badge {{
        display:inline-block;
        background:rgba(255,255,255,0.15);
        padding:6px 14px;
        border-radius:999px;
        font-size:13px;
        font-weight:600;
        margin-bottom:12px;
    }}

    .hero h1 {{
            margin: 0;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        .hero p {{
            margin: 10px 0 0 0;
            color: rgba(255,255,255,0.88);
            font-size: 1rem;
            max-width: 850px;
        }}

    .metric-card {{
        background:white;
        border-radius:22px;
        padding:20px;
        border:1px solid #dfe8ec;
        box-shadow:0 6px 18px rgba(0,0,0,0.04);
    }}

    .metric-title {{
        font-size:14px;
        color:#6b7280;
    }}

    .metric-value {{
        font-size:26px;
        font-weight:800;
        color:#142230;
        margin-top:6px;
    }}

    .metric-sub {{
        font-size:13px;
        color:#7b8794;
    }}

    footer {{
        visibility:hidden;
    }}
    button[data-baseweb="tab"]{{
        background:white !important;
        border:1px solid #dfe8ec !important;
        border-radius:14px !important;
        padding:10px 18px !important;
        margin-right:8px !important;
        color:#334155 !important;
        font-weight:700 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"]{{
        background:#0f172a !important;
        color:white !important;
        border-color:#0f172a !important;
    }}
    .chart-card{{
        background:white;
        border:1px solid #dfe8ec;
        border-radius:22px;
        padding:14px 14px 8px 14px;
        box-shadow:0 6px 18px rgba(0,0,0,.04);
        margin-bottom:16px;
    }}

    .chart-title{{
        font-size:15px;
        font-weight:800;
        color:#1e293b;
        margin-bottom:10px;
    }}
    .eda-card{{
    background:white;
    border:1px solid #dbe3ef;
    border-radius:22px;
    padding:18px;
    margin-bottom:20px;
    box-shadow:0 2px 8px rgba(0,0,0,0.04);
    }}

    .eda-title{{
    font-size:20px;
    font-weight:800;
    color:#1e293b;
    margin-bottom:10px;
    }}
    .chart-card{{
        background:white;
        border:1px solid #dbe3ef;
        border-radius:22px;
        padding:14px;
        margin-bottom:18px;
    }}

    .chart-title{{
        font-size:16px;
        font-weight:700;
        color:#1e293b;
        margin-bottom:8px;
    }}

    [data-testid="column"]{{
        gap:18px;
    }}
    div[data-testid="stPlotlyChart"]{{
        background:white;
        border-radius:0 0 22px 22px;
        padding:10px;
        border:1px solid #dbe3ef;
        border-top:none;
        margin-top:-8px;
    }}
    /* ===== KPI CARDS HOVER EFFECT ===== */

    .metric-card {{
        background: white;
        border-radius: 22px;
        padding: 20px;
        border: 1px solid #dfe8ec;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
        transition: all 0.35s ease;
        cursor: pointer;
    }}

    /* 🔥 HOVER EFFECT (MAIN MAGIC) */
    .metric-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(37, 99, 235, 0.15);
        border-color: rgba(37, 99, 235, 0.25);
    }}

    /* TEXT ENHANCEMENT ON HOVER */
    .metric-card:hover .metric-title {{
        color: #2563eb;
    }}

    .metric-card:hover .metric-value {{
        color: #0f172a;
    }}

    /* OPTIONAL: subtle glow */
    .metric-card:hover {{
        background: linear-gradient(
            180deg,
            #ffffff 0%,
            #f8fafc 100%
        );
    }}
    /* ===== PREMIUM GLOWING TABS ===== */

    button[data-baseweb="tab"] {{
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 18px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-right: 10px !important;
        transition: all 0.35s ease !important;
        position: relative;
        overflow: hidden;
    }}

    /* 🔥 HOVER GLOW */
    button[data-baseweb="tab"]:hover {{
        transform: translateY(-3px) scale(1.02);
        border-color: #2563eb !important;
        box-shadow: 
            0 0 10px rgba(37, 99, 235, 0.25),
            0 0 25px rgba(37, 99, 235, 0.15),
            0 10px 25px rgba(0,0,0,0.08);
        color: #2563eb !important;
    }}

    /* 🔥 ACTIVE TAB (MAIN GLOW) */
    button[data-baseweb="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        color: #ffffff !important;
        border: none !important;
        transform: scale(1.05);
        box-shadow:
            0 0 15px rgba(59,130,246,0.5),
            0 0 30px rgba(59,130,246,0.3),
            0 10px 30px rgba(0,0,0,0.25);
    }}

    /* ✨ INNER GLOW EFFECT */
    button[data-baseweb="tab"][aria-selected="true"]::before {{
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 18px;
        background: radial-gradient(circle at top left, rgba(59,130,246,0.4), transparent 70%);
        opacity: 0.6;
        pointer-events: none;
    }}

    /* 🚫 REMOVE DEFAULT LINE */
    div[data-baseweb="tab-list"] {{
        border-bottom: none !important;
    }}

    </style>
    """, unsafe_allow_html=True)



    # ======================================================
    # SIDEBAR
    # ======================================================
    st.sidebar.markdown("### MARKET FILTERS")

    states = ["All"] + sorted(df["State"].dropna().astype(str).unique())
    selected_state = st.sidebar.selectbox("State", states)

    fdf = df.copy()

    if selected_state != "All":
        fdf = fdf[fdf["State"] == selected_state]

    cities = ["All"] + sorted(fdf["City"].dropna().astype(str).unique())
    selected_city = st.sidebar.selectbox("City", cities)

    if selected_city != "All":
        fdf = fdf[fdf["City"] == selected_city]

    localities = ["All"] + sorted(fdf["Locality"].dropna().astype(str).unique())
    selected_locality = st.sidebar.selectbox("Locality", localities)

    if selected_locality != "All":
        fdf = fdf[fdf["Locality"] == selected_locality]
    # ======================================================
    # CLEAN DATA FOR TAB 4 (FIX UNKNOWN ISSUE)
    # ======================================================

    # Replace "Unknown" → NaN
    # Convert to numeric
    # Create clean dataframe (DON’T DROP EVERYTHING)
    fdf_clean = fdf.copy()

    # Fill missing instead of dropping
    fdf_clean["Parking_Space"] = fdf_clean["Parking_Space"].fillna("Unknown").astype(str)
    fdf_clean["Public_Transport_Accessibility"] = fdf_clean["Public_Transport_Accessibility"].fillna("Unknown").astype(str)


    st.sidebar.markdown("###  MARKET INTELLIGENCE PANEL")

    avg_price = fdf["Price_in_Lakhs"].mean()
    avg_sqft = fdf["Size_in_SqFt"].mean()

    score = min(100, int(avg_price / 4))
    yield_est = round(avg_price / max(avg_sqft,1), 2)

    hotspot = "High" if score > 70 else "Medium" if score > 40 else "Emerging"

    st.sidebar.info(f"Selected Region Score: {score}/100")
    st.sidebar.success(f"Avg Price: ₹ {avg_price:.1f}L")
    st.sidebar.warning(f"Growth Potential: {score}%")
    st.sidebar.info(f"Rental Yield Estimate: {yield_est}%")
    st.sidebar.error(f"Investment Hotspot Meter: {hotspot}")


    # ======================================================
    # HERO
    # ======================================================
    st.markdown("""
    <div class="hero">
        <div class="badge">EDA Intelligence Suite</div>
        <h1>Real Estate Exploratory Dashboard</h1>
        <p>
            Analyze price trends, locality signals, feature relationships and ownership patterns
            across the real estate market.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ======================================================
    # KPI ROW
    # ======================================================
    avg_price = fdf["Price_in_Lakhs"].mean()
    avg_size = fdf["Size_in_SqFt"].mean()
    cities_cov = fdf["City"].nunique()
    avg_psf = fdf["Price_per_SqFt"].mean()

    total_props = len(fdf)

    k1,k2,k3,k4,k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Price</div>
            <div class="metric-value">₹ {avg_price:.1f}L</div>
            <div class="metric-sub">Filtered dataset</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Size</div>
            <div class="metric-value">{avg_size:.0f}</div>
            <div class="metric-sub">SqFt</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Cities Covered</div>
            <div class="metric-value">{cities_cov}</div>
            <div class="metric-sub">Locations</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Price/SqFt</div>
            <div class="metric-value">{avg_psf:.2f}</div>
            <div class="metric-sub">Efficiency metric</div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Properties</div>
            <div class="metric-value">{total_props:,}</div>
            <div class="metric-sub">Live inventory</div>
        </div>
        """, unsafe_allow_html=True) 

    st.markdown("<br>", unsafe_allow_html=True)

    # ======================================================
    # TABS
    # ======================================================
    tab1,tab2,tab3,tab4 = st.tabs([
        "1–5 Price & Size",
        "6–10 Location",
        "11–15 Correlation",
        "16–20 Ownership"
    ])

    # ======================================================
    # TAB 1
    # ======================================================

    with tab1:
        st.markdown("""
        <style>
        .st-key-price-card {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-price-card .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .st-key-price-card div[data-testid="stPlotlyChart"] {
            background: white;
            border-radius: 16px;
            overflow: hidden;
        }
        /* remove the inner grey outline */
        .st-key-price-card div[data-testid="stPlotlyChart"] {
        background: transparent;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible;
        }       
        .st-key-size-card {
        background: white;
        border: 1px solid #dbe3ef;
        border-radius: 22px;
        padding: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-size-card .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }    
        .st-key-size-card div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin-top: 0 !important;
            box-shadow: none !important;
        }   
        .st-key-type-card {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-type-card .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .st-key-type-card div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
        } 
        .st-key-scatter-card {
        background: white;
        border: 1px solid #dbe3ef;
        border-radius: 22px;
        padding: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-scatter-card .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .st-key-scatter-card div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
        }
        .st-key-outlier-card {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-outlier-card .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .st-key-outlier-card div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
        }        
        .st-key-outlier-card {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }
        .chart-title {
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }

        .st-key-tab2-card-6,
        .st-key-tab2-card-7,
        .st-key-tab2-card-8,
        .st-key-tab2-card-9,
        .st-key-tab2-card-10 {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-tab2-card-6 div[data-testid="stPlotlyChart"],
        .st-key-tab2-card-7 div[data-testid="stPlotlyChart"],
        .st-key-tab2-card-8 div[data-testid="stPlotlyChart"],
        .st-key-tab2-card-9 div[data-testid="stPlotlyChart"],
        .st-key-tab2-card-10 div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
        }
        .st-key-tab3-card-11,
        .st-key-tab3-card-12,
        .st-key-tab3-card-13,
        .st-key-tab3-card-14,
        .st-key-tab3-card-15 {
            background: white;
            border: 1px solid #dbe3ef;
            border-radius: 22px;
            padding: 14px;
            margin-bottom: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,.04);
        }

        .st-key-tab3-card-11 div[data-testid="stPlotlyChart"],
        .st-key-tab3-card-12 div[data-testid="stPlotlyChart"],
        .st-key-tab3-card-13 div[data-testid="stPlotlyChart"],
        .st-key-tab3-card-14 div[data-testid="stPlotlyChart"],
        .st-key-tab3-card-15 div[data-testid="stPlotlyChart"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 0 !important;
        }
                    .st-key-tab4-card-16,
    .st-key-tab4-card-17,
    .st-key-tab4-card-18,
    .st-key-tab4-card-19,
    .st-key-tab4-card-20 {
        background: white;
        border: 1px solid #dbe3ef;
        border-radius: 22px;
        padding: 14px;
        margin-bottom: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,.04);
    }

    .st-key-tab4-card-16 div[data-testid="stPlotlyChart"],
    .st-key-tab4-card-17 div[data-testid="stPlotlyChart"],
    .st-key-tab4-card-18 div[data-testid="stPlotlyChart"],
    .st-key-tab4-card-19 div[data-testid="stPlotlyChart"],
    .st-key-tab4-card-20 div[data-testid="stPlotlyChart"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
    }
                
        </style>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        # ==================================================
        with c1:
            with st.container(key="price-card"):
                st.markdown('<div class="chart-title">1. Distribution of Property Prices</div>', unsafe_allow_html=True)

                bins = ["50-100L","100-150L","150-200L","200-250L","250-300L","300-350L","350-400L","400-450L"]
                vals = [45,78,92,105,98,67,42,28]

                fig = px.bar(x=bins, y=vals)

                fig.update_traces(marker_color="#0f766e", marker_line_width=0)

                fig.update_layout(
                    height=290,
                    margin=dict(t=5, l=40, r=10, b=40),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(tickangle=-25, showgrid=True, zeroline=True, showline=True, linecolor="#000000", tickfont=dict(color="#000000"), title=""),
                    yaxis=dict(
                        range=[0,120],
                        dtick=30,
                        gridcolor="#dbe3ef",
                        zeroline=True,
                        showline=True,
                        linecolor="#000000",
                        griddash="dot",
                        tickfont=dict(color="#000000"),
                        title=""
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)

        # ==================================================
        with c2:
            with st.container(key="size-card"):
                st.markdown(
                    '<div class="chart-title">2. Distribution of Property Sizes</div>',
                    unsafe_allow_html=True
                )

                bins = [
                    "300-800 SqFt","800-1200 SqFt","1200-1800 SqFt",
                    "1800-2400 SqFt","2400-3000 SqFt","3000-3600 SqFt","3600-4200 SqFt"
                ]
                vals = [62, 105, 118, 95, 68, 45, 22]

                fig = px.bar(x=bins, y=vals)

                fig.update_traces(
                    marker_color="#2563eb",
                    marker_line_width=0
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=5, l=40, r=10, b=40),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        tickangle=-25,
                        showgrid=True,
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        range=[0,120],
                        dtick=30,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)

        # ==================================================
        c3,c4 = st.columns(2)

        with c3:
            with st.container(key="type-card"):
                st.markdown(
                    '<div class="chart-title">3. Price per SqFt by Property Type</div>',
                    unsafe_allow_html=True
                )

                fig = px.bar(
                    x=["Villa", "Independent House", "Apartment"],
                    y=[185, 172, 145]
                )

                fig.update_traces(
                    marker_color="#ea580c",
                    marker_line_width=0
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=5, l=40, r=10, b=40),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000")
                    ),
                    yaxis=dict(
                        range=[0, 200],
                        dtick=50,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000"),
                        zeroline=True
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)

        # ==================================================
        with c4:
            with st.container(key="scatter-card"):
                st.markdown(
                    '<div class="chart-title">4. Size vs Price Relationship</div>',
                    unsafe_allow_html=True
                )

                fig = px.scatter(
                    fdf.sample(min(len(fdf), 220)),
                    x="Size_in_SqFt",
                    y="Price_in_Lakhs"
                )

                fig.update_traces(
                    marker=dict(
                        size=6,
                        color="#3b82f6",
                        opacity=0.55
                    )
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=5, l=40, r=10, b=40),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        range=[0, 6000],
                        dtick=1500,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="Size (SqFt)",
                        title_font=dict(color="#000000", size=12),
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000"),
                        zeroline=True
                    ),
                    yaxis=dict(
                        range=[0, 600],
                        dtick=150,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="Price (Lakhs)",
                        title_font=dict(color="#000000", size=12),
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000"),
                        zeroline=True
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)

        # ==================================================
        with c3:
            with st.container(key="outlier-card"):
                st.markdown(
                    '<div class="chart-title">5. Outliers in Price per SqFt</div>',
                    unsafe_allow_html=True
                )

                sample_df = fdf.sample(min(len(fdf), 240)).reset_index(drop=True)
                sample_df["pos"] = np.linspace(0, 250, len(sample_df))

                fig = px.scatter(
                    sample_df,
                    x="pos",
                    y="Price_in_Lakhs"
                )

                fig.update_traces(
                    marker=dict(
                        size=7,
                        color="#07524C",
                        opacity=0.75
                    )
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=5, l=40, r=10, b=20),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        range=[0, 250],
                        dtick=65,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000"),
                        zeroline=True
                    ),
                    yaxis=dict(
                        range=[0, 600],
                        dtick=150,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000"),
                        zeroline=True
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None)

    # ======================================================
    # TAB 2
    # ======================================================
    with tab2:

        c1, c2 = st.columns(2)

        with c1:
            with st.container(key="tab2-card-6"):
                st.markdown(
                    '<div class="chart-title">6. Avg Price per SqFt by State</div>',
                    unsafe_allow_html=True
                )

                temp = (
                    fdf.groupby("State", as_index=False)["Price_per_SqFt"]
                    .mean()
                    .sort_values("Price_per_SqFt", ascending=False)
                    .head(8)
                )

                fig = px.bar(
                    temp,
                    x="State",
                    y="Price_per_SqFt",
                    color_discrete_sequence=["#3b82f6"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        tickangle=-25,
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        with c2:
            with st.container(key="tab2-card-7"):
                st.markdown(
                    '<div class="chart-title">7. Average Property Price by City</div>',
                    unsafe_allow_html=True
                )

                temp = (
                    fdf.groupby("City", as_index=False)["Price_in_Lakhs"]
                    .mean()
                    .sort_values("Price_in_Lakhs", ascending=False)
                    .head(10)
                )

                fig = px.bar(
                    temp,
                    x="City",
                    y="Price_in_Lakhs",
                    color="Price_in_Lakhs",
                    color_continuous_scale=["#f9c7f1", "#530488"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    coloraxis_showscale=False,
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    xaxis=dict(
                        tickangle=-30,
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        c3, c4 = st.columns(2)
        
        with c3:
            with st.container(key="tab2-card-8"):
                st.markdown(
                    '<div class="chart-title">8. Median Age by Locality</div>',
                    unsafe_allow_html=True
                )

                temp = (
                    fdf.groupby("Locality", as_index=False)["Age_of_Property"]
                    .median()
                    .head(15)
                )

                fig = px.bar(
                    temp,
                    x="Locality",
                    y="Age_of_Property",
                    color_discrete_sequence=["#bf104e"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        tickangle=-35,
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        with c4:
            with st.container(key="tab2-card-9"):
                st.markdown(
                    '<div class="chart-title">9. BHK Distribution Across Cities</div>',
                    unsafe_allow_html=True
                )

                temp = (
                    fdf.groupby(["City", "BHK"])
                    .size()
                    .reset_index(name="Count")
                )

                fig = px.bar(
                    temp.head(25),
                    x="City",
                    y="Count",
                    color="BHK",
                    barmode="stack",
                    color_continuous_scale=["#dcdbfe", "#93c5fd", "#60a5fa", "#38bdf8", "#2563eb"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    legend_title_text="BHK",
                    xaxis=dict(
                        tickangle=-25,
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000")
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        linewidth=1,
                        tickfont=dict(color="#000000")
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

            with c3:
                with st.container(key="tab2-card-10"):
                    st.markdown(
                        '<div class="chart-title">10. Top Expensive Localities</div>',
                        unsafe_allow_html=True
                    )

                    temp = (
                        fdf.groupby("Locality", as_index=False)["Price_in_Lakhs"]
                        .mean()
                        .sort_values("Price_in_Lakhs", ascending=False)
                        .head(8)
                    )

                    fig = px.line(
                        temp,
                        x="Locality",
                        y="Price_in_Lakhs",
                        markers=True
                    )

                    fig.update_traces(
                        line_color="#0f766e",
                        marker=dict(size=8, color="#ea580c")
                    )

                    fig.update_layout(
                        height=340,
                        margin=dict(t=10, l=10, r=10, b=10),
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        showlegend=False,
                        xaxis=dict(
                            tickangle=-25,
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        theme=None,
                        config={"displayModeBar": False}
                    )


    # ======================================================
    # TAB 3
    # ======================================================
    with tab3:

        corr_cols = [
        "Price_in_Lakhs", "Size_in_SqFt", "Price_per_SqFt",
        "Age_of_Property", "Nearby_Schools", "Nearby_Hospitals",
        ]
        short_labels = ["Price", "Size", "Price/SqFt", "Age", "Schools", "Hospitals"]

        corr = fdf[num_cols].corr(numeric_only=True)

        # ── 11. Numeric Correlation Matrix ─────────────────────────────────────
        with st.container(key="tab3-card-11"):
            st.markdown(
                '<div class="chart-title">11. Numeric Correlation Matrix</div>',
                unsafe_allow_html=True
            )

            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=short_labels,
                y=short_labels,
                text=corr.round(2).values,
                texttemplate="%{text:.2f}",
                textfont=dict(size=12),
                colorscale=[
                    [0.00, "#f0fdf9"],
                    [0.20, "#ccfbf1"],
                    [0.40, "#5eead4"],
                    [0.60, "#2dd4bf"],
                    [0.75, "#0d9488"],
                    [0.85, "#0f766e"],
                    [1.00, "#134e4a"],
                ],
                zmin=0,
                zmax=1,
                showscale=False,
                xgap=4,
                ygap=4,
            ))

            fig.update_layout(
                height=290,
                margin=dict(t=10, l=10, r=10, b=10),
                paper_bgcolor="white",
                plot_bgcolor="white",
                xaxis=dict(
                    side="top",
                    tickfont=dict(size=12, color="#000000"),
                    showline=False,
                    showgrid=False,
                ),
                yaxis=dict(
                    autorange="reversed",
                    tickfont=dict(size=12, color="#000000"),
                    showline=False,
                    showgrid=False,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                theme=None,
                config={"displayModeBar": False}
            )

        # ── 12 & 13. Scatter plots ─────────────────────────────────────────────
        c1, c2 = st.columns(2)

        with c1:
            with st.container(key="tab3-card-12"):
                st.markdown(
                    '<div class="chart-title">12. Schools vs Price/SqFt</div>',
                    unsafe_allow_html=True
                )

                fig = px.scatter(
                    fdf.sample(min(len(fdf), 250)),
                    x="Nearby_Schools",
                    y="Price_per_SqFt",
                    opacity=0.6,
                    color_discrete_sequence=["#2563eb"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        with c2:
            with st.container(key="tab3-card-13"):
                st.markdown(
                    '<div class="chart-title">13. Hospitals vs Price/SqFt</div>',
                    unsafe_allow_html=True
                )

                fig = px.scatter(
                    fdf.sample(min(len(fdf), 250)),
                    x="Nearby_Hospitals",
                    y="Price_per_SqFt",
                    opacity=0.6,
                    color_discrete_sequence=["#0f766e"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        # ── 14 & 15. Box plots ─────────────────────────────────────────────────
        c3, c4 = st.columns(2)

        with c3:
            with st.container(key="tab3-card-14"):
                st.markdown(
                    '<div class="chart-title">14. Price by Furnished Status</div>',
                    unsafe_allow_html=True
                )

                fig = px.box(
                    fdf,
                    x="Furnished_Status",
                    y="Price_in_Lakhs",
                    color="Furnished_Status",
                    color_discrete_sequence=["#ea580c", "#2563eb", "#0f766e"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )

        with c4:
            with st.container(key="tab3-card-15"):
                st.markdown(
                    '<div class="chart-title">15. Facing vs Price/SqFt</div>',
                    unsafe_allow_html=True
                )

                fig = px.box(
                    fdf,
                    x="Facing",
                    y="Price_per_SqFt",
                    color="Facing",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    theme=None,
                    config={"displayModeBar": False}
                )
    # ======================================================
    # TAB 4
    # ======================================================
    with tab4:

        c1, c2 = st.columns(2)

        # ── 16. Owner Type Distribution ────────────────────────────────────────
        with c1:
            with st.container(key="tab4-card-16"):
                st.markdown(
                    '<div class="chart-title">16. Owner Type Distribution</div>',
                    unsafe_allow_html=True
                )

                owner = fdf["Owner_Type"].value_counts().reset_index()
                owner.columns = ["Owner_Type", "Count"]

                fig = px.bar(
                    owner,
                    x="Owner_Type",
                    y="Count",
                    color_discrete_sequence=["#0f766e"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})

        # ── 17. Availability Status ────────────────────────────────────────────
        with c2:
            with st.container(key="tab4-card-17"):
                st.markdown(
                    '<div class="chart-title">17. Availability Status</div>',
                    unsafe_allow_html=True
                )

                avail = fdf["Availability_Status"].value_counts().reset_index()
                avail.columns = ["Availability_Status", "Count"]

                fig = px.bar(
                    avail,
                    x="Availability_Status",
                    y="Count",
                    color_discrete_sequence=["#2563eb"]
                )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="",
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})

        # ── 18 & 19 ────────────────────────────────────────────────────────────
        c3, c4 = st.columns(2)

        with c3:
            with st.container(key="tab4-card-18"):
                st.markdown(
                    '<div class="chart-title">18. Parking vs Price</div>',
                    unsafe_allow_html=True
                )

                # Handle NaN in Parking_Space - fill with "Unknown" instead of dropping
                parking_df = fdf[["Parking_Space", "Price_in_Lakhs"]].copy()
                parking_df["Parking_Space"] = parking_df["Parking_Space"].fillna("Unknown")
                parking_df["Price_in_Lakhs"] = pd.to_numeric(parking_df["Price_in_Lakhs"], errors="coerce")
                # Only drop if Price is NaN
                parking_df = parking_df.dropna(subset=["Price_in_Lakhs"])

                if len(parking_df) > 0:
                    fig = px.box(
                        parking_df,
                        x="Parking_Space",
                        y="Price_in_Lakhs",
                        color="Parking_Space",
                    )
                    fig.update_traces(
                        hoverlabel=dict(
                        bgcolor="#636EFA",
                        font_size=13,
                    )
                )

                    fig.update_layout(
                        height=290,
                        margin=dict(t=10, l=10, r=10, b=10),
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        showlegend=False,
                        xaxis=dict(
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data for Parking vs Price")

        with c4:
            with st.container(key="tab4-card-19"):
                st.markdown(
                    '<div class="chart-title">19. Security vs Price</div>',
                    unsafe_allow_html=True
                )

                security_df = fdf[["Security", "Price_in_Lakhs"]].copy()
                security_df["Security"] = security_df["Security"].fillna("Unknown")
                security_df["Price_in_Lakhs"] = pd.to_numeric(security_df["Price_in_Lakhs"], errors="coerce")
                security_df = security_df[security_df["Price_in_Lakhs"].notna()]

                if len(security_df) > 0:
                    fig = px.box(
                        security_df,
                        x="Security",
                        y="Price_in_Lakhs",
                        color_discrete_sequence=["#22c55e"]
                    )
                    fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="#22c55e",
                    font_size=13,
                    )
                )

                    fig.update_layout(
                        height=290,
                        margin=dict(t=10, l=10, r=10, b=10),
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        showlegend=False,
                        xaxis=dict(
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        ),
                        yaxis=dict(
                            showgrid=True,
                            gridcolor="#dbe3ef",
                            griddash="dot",
                            title="",
                            showline=True,
                            linecolor="black",
                            tickfont=dict(color="#000000"),
                            linewidth=1
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})
                else:
                    st.warning("No data for Security vs Price")

        with st.container(key="tab4-card-20"):
            st.markdown(
                '<div class="chart-title">20. Public Transport vs Price Potential</div>',
                unsafe_allow_html=True
            )

            transport_df = fdf[["Public_Transport_Accessibility", "Price_per_SqFt"]].copy()
            transport_df["Public_Transport_Accessibility"] = transport_df["Public_Transport_Accessibility"].fillna("Unknown")
            transport_df["Price_per_SqFt"] = pd.to_numeric(transport_df["Price_per_SqFt"], errors="coerce")
            transport_df = transport_df.dropna(subset=["Price_per_SqFt"])

            if len(transport_df) > 0:
                fig = px.box(
                    transport_df,
                    x="Public_Transport_Accessibility",
                    y="Price_per_SqFt",
                    color="Public_Transport_Accessibility"
                )
                fig.update_traces(
                    hoverlabel=dict(
                    bgcolor="#636EFA",
                    font_size=13,
                )
            )

                fig.update_layout(
                    height=290,
                    margin=dict(t=10, l=10, r=10, b=10),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="Transport Accessibility",
                        title_font=dict(color="#000000", size=11),
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="#dbe3ef",
                        griddash="dot",
                        title="Price/SqFt",
                        title_font=dict(color="#000000", size=11),
                        showline=True,
                        linecolor="black",
                        tickfont=dict(color="#000000"),
                        linewidth=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data for Public Transport vs Price")

    # ======================================================
    # FOOTER
    # ======================================================
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="
        text-align:center;
        color:#64748b;
        font-size:14px;
        padding:18px 0 10px 0;
    ">
    Real Estate EDA Dashboard • Unified Experience with Home Dashboard
    </div>
    """, unsafe_allow_html=True)