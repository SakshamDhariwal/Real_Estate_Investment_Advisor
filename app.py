import streamlit.components.v1 as components
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
import time
import base64
from theme import render_sidebar_brand
from fpdf import FPDF
from streamlit_option_menu import option_menu
from pathlib import Path
from components import render_hero


def get_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = Path("assets/building.png").resolve()

st.set_page_config(
    page_title="Real Estate Investment Advisor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# PREMIUM TOP NAVBAR
# ===============================

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown("""
<style>
            /* Hide Streamlit default top bar */
header[data-testid="stHeader"]{
    visibility:hidden;
    height:0px;
}

div[data-testid="stToolbar"]{
    display:none;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

.topnav-btn button{
    height:58px !important;
    border-radius:16px !important;
    font-weight:700 !important;
    font-size:15px !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    background:linear-gradient(135deg,#0b1220,#111827) !important;
    color:white !important;
    transition:0.3s ease;
}
.topnav-btn button:hover{
    border:1px solid #2563eb !important;
    box-shadow:0 8px 22px rgba(37,99,235,.25) !important;
    transform:translateY(-1px);
}
.brand-wrap{
    background:linear-gradient(135deg,#07111f,#0b1830);
    padding:14px 18px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.06);
    box-shadow:0 12px 28px rgba(0,0,0,.18);
}
.brand-title{
    font-size:24px;
    font-weight:800;
    color:white;
    line-height:1.1;
}
.brand-sub{
    font-size:11px;
    color:#94a3b8;
    margin-top:2px;
}
.top-navbar{
    position:fixed;
    top:0;
    left:0;
    right:0;
    height:78px;
    z-index:9999;
    background:linear-gradient(90deg,#020617,#03152f,#041c39);
    border-bottom:1px solid rgba(255,255,255,.08);

    display:grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items:center;

    padding:0 20px;
}
section[data-testid="stSidebar"]{
    z-index:10 !important;
}  
.main .block-container{
    padding-top:110px !important;
}
section[data-testid="stSidebar"] > div:first-child{
    padding-top:95px !important;
}
.nav-left{
    display:flex;
    align-items:center;
    gap:14px;
    justify-content:flex-start;
}

.nav-center{
    display:flex;
    justify-content:center;
    gap:14px;
}

.nav-right{
    display:flex;
    justify-content:flex-end;
}

.nav-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    height:48px;
    padding:0 22px;
    border-radius:14px;
    background:#0b0f19;
    color:white !important;
    font-weight:700;
    font-size:15px;
    text-decoration:none !important;
    border:1px solid rgba(255,255,255,.08);
}

.nav-btn:hover{
    border:1px solid #2563eb;
    box-shadow:0 8px 22px rgba(37,99,235,.25);
}

/* Hide sidebar collapse arrow button */
button[kind="header"],
[data-testid="collapsedControl"]{
    display:none !important;
}

/* Keep sidebar permanently visible */
section[data-testid="stSidebar"]{
    transform:none !important;
    visibility:visible !important;
}  
/* Remove sidebar collapse button completely */
[data-testid="collapsedControl"],
button[kind="header"]{
    display:none !important;
}

/* Remove extra top padding inside sidebar */
section[data-testid="stSidebar"] > div:first-child{
    padding-top: 30px !important;
}

/* Sidebar content starts tighter */
section[data-testid="stSidebar"] .block-container{
    padding-top: 0.6rem !important;
    margin-top: 0rem !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] .brand-sub{
    margin-bottom:8px !important;
}
.main .block-container{
    padding-top:95px !important;
}
.nav-btn:hover{
    transform:translateY(-2px);
    box-shadow:0 10px 24px rgba(59,130,246,.25);
}         
      
</style>
""", unsafe_allow_html=True)

# ---- Build navbar HTML as a plain variable first ----
logo_b64 = get_base64('assets/logo.png')

navbar_html = (
    '<div style="'
    'position:fixed;top:0;left:0;right:0;height:78px;z-index:9999;'
    'background:linear-gradient(90deg,#020617 25%,#061327 50%,#0b1f3a 100%);'
    'display:flex;align-items:center;justify-content:space-between;'
    'padding:0 22px;border-bottom:1px solid rgba(255,255,255,.08);">'

    # LEFT: Brand
    '<div style="display:flex;align-items:center;gap:12px;color:white;">'
    '<img src="data:image/png;base64,' + logo_b64 + '" '
    'style="width:52px;height:52px;object-fit:contain;">'
    '<div>'
    '<div style="font-size:18px;font-weight:800;">RealEstate Investment Advisor</div>'
    '<div style="font-size:11px;color:#94a3b8;">Predicting Property Profitability &amp; Future Value</div>'
    '</div></div>'

    # RIGHT: Nav Buttons
    '<div style="display:flex;gap:12px;align-items:center;">'

    '<a href="?page=Home" target="_self" style="'
    'display:flex;align-items:center;height:44px;padding:0 22px;border-radius:12px;'
    'background:#0b0f19;color:white;font-weight:700;font-size:14px;'
    'text-decoration:none;border:1px solid rgba(255,255,255,.12);">⌂ Home</a>'

    '<a href="?page=EDA+Insights" target="_self" style="'
    'display:flex;align-items:center;height:44px;padding:0 22px;border-radius:12px;'
    'background:#0b0f19;color:white;font-weight:700;font-size:14px;'
    'text-decoration:none;border:1px solid rgba(255,255,255,.12);">▮▮▮ EDA Insights</a>'

    '<a id="dl-btn" href="#" style="'
    'display:flex;align-items:center;height:44px;padding:0 22px;'
    'border-radius:12px;background:#1d4ed8;color:white;font-weight:700;'
    'font-size:14px;text-decoration:none;border:1px solid rgba(255,255,255,.12);cursor:pointer;"'
    'onclick="...">'
    '&#8595; Download</a>'

    '</div></div>'
)

st.markdown(navbar_html, unsafe_allow_html=True)

# Handle page navigation via query params
params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

selected = st.session_state.page

# PDF bytes ready karo — dummy data se shuru, Home page override karega
import io
_pdf_placeholder = io.BytesIO(b"placeholder")

st.markdown("""
<style>
/* Sirf download button ko navbar mein fix karo */
[data-testid="stDownloadButton"] {
    position: fixed !important;
    top: 17px !important;
    right: 22px !important;
    z-index: 99999 !important;
    width: fit-content !important;
}
[data-testid="stDownloadButton"] button {
    height: 44px !important;
    padding: 0 22px !important;
    border-radius: 12px !important;
    background: #142d4c !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    width: auto !important;
}
</style>
""", unsafe_allow_html=True)

st.download_button(
    label="⤓ Download",
    data=_pdf_placeholder,
    file_name="investment_report.pdf",
    mime="application/pdf",
    key="top_dl_btn"
)

img64 = get_base64("assets/building.png")

st.markdown(f"""
<style>

section[data-testid="stSidebar"] {{
    min-width: 320px !important;
    max-width: 320px !important;
}}

section[data-testid="stSidebar"] > div:first-child {{
    background:
    linear-gradient(
        180deg,
        rgba(5,8,35,0.40) 0%,
        rgba(15,10,60,0.35) 45%,
        rgba(5,8,35,0.55) 100%
    ),
    url("data:image/png;base64,{img64}");

    background-size: cover !important;
    background-position: center top !important;
    background-repeat: no-repeat !important;
}}

section[data-testid="stSidebar"] .block-container {{
    background: transparent !important;
    padding-top: 1rem;
}}

section[data-testid="stSidebar"] * {{
    color: white !important;
}}

section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider,
section[data-testid="stSidebar"] .stButton {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 8px;
    backdrop-filter: blur(10px);
    margin-bottom: 10px;
}}

section[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    border-radius: 14px;
    border: none;
    font-weight: 700;
    color: white;
    background: linear-gradient(135deg,#0f766e,#2563eb);
}}

</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "cleaned_data.csv"
MODELS_DIR = BASE_DIR / "models"


@st.cache_data
def load_data():
    url = "https://drive.google.com/uc?id=1foeVNmPwfuwKFtTIVFYrgmPsyaXar9CK"
    return pd.read_csv(url)


import requests
import joblib
import tempfile

@st.cache_resource
def load_artifacts():

    def load_model(url):
        response = requests.get(url)
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(response.content)
            return joblib.load(tmp.name)

    clf = load_model("https://drive.google.com/file/d/1f_9yxV1x9NfRarwzdMOWMagkBZTHI758")
    reg = load_model("https://drive.google.com/file/d/18rR1_pQC1v63svYniziBjH1ziM7Wq4Qs")
    encoders = load_model("https://drive.google.com/file/d/1Ki37DQ9dP1kjnTERsWHcADIf2U09NNMF")

    return clf, reg, encoders


df = load_data()
#st.write(df.head())
clf, reg, encoders = load_artifacts()

# =============================
# SESSION STATE INIT
# =============================
if "pred_data" not in st.session_state:
    st.session_state.pred_data = None

# =============================
# CREATE FILTERS FIRST
# =============================

state_options = sorted(df["State"].dropna().astype(str).unique())
selected_state = st.sidebar.selectbox("State", state_options)

city_options = sorted(
    df[df["State"].astype(str) == selected_state]["City"]
    .dropna().astype(str).unique()
)
selected_city = st.sidebar.selectbox("City", city_options)

locality_options = sorted(
    df[df["City"].astype(str) == selected_city]["Locality"]
    .dropna().astype(str).unique()
)
selected_locality = st.sidebar.selectbox("Locality", locality_options)
ptype_options = sorted(df["Property_Type"].dropna().astype(str).unique())
selected_ptype = st.sidebar.selectbox("Property Type", ptype_options)

# create filtered FIRST
filtered = df[
    (df["State"].astype(str) == selected_state)
    & (df["City"].astype(str) == selected_city)
    & (df["Locality"].astype(str) == selected_locality)
]

#HOME DASHBOARD
if selected == "Home":

    def build_premium_sidebar():
        st.sidebar.markdown("""
        <div style="
            padding:18px;
            border-radius:20px;
            margin-bottom:18px;
            background:linear-gradient(135deg,#0f766e,#2563eb);
            box-shadow:0 14px 28px rgba(37,99,235,.25);
            ">
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        """
    <style>
    :root {
        --bg1: #eef7f7;
        --bg2: #f8fbfc;
        --card: #ffffff;
        --text: #142330;
        --muted: #60707c;
        --border: #d9e5ea;
        --teal: #0f766e;
        --teal-dark: #115e59;
        --blue: #2563eb;
        --orange: #ea580c;
        --green: #16a34a;
        --red: #dc2626;
        --shadow: 0 12px 28px rgba(15, 23, 42, 0.07);
    }

    html, body, [class*="css"] {
        font-family: "Avenir Next", "Segoe UI", sans-serif;
    }

    .stApp {
        background:#eef3f4;
        background: linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 100%);
    }

    section[data-testid="stSidebar"] *{
        color:white !important;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    .hero {
        background: linear-gradient(135deg, #0f766e 0%, #164e63 50%, #1d4ed8 100%);
        color: white;
        border-radius: 26px;
        padding: 30px 32px;
        margin-bottom: 18px;
        box-shadow: 0 18px 40px rgba(15, 118, 110, 0.18);
        margin-top: -20px;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .hero p {
        margin: 10px 0 0 0;
        color: rgba(255,255,255,0.88);
        font-size: 1rem;
        max-width: 850px;
    }
    /* 🔥 HOVER EFFECT (MAIN MAGIC) */
.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(37, 99, 235, 0.15);
    border-color: rgba(37, 99, 235, 0.25);
}

/* TEXT ENHANCEMENT ON HOVER */
.metric-card:hover .metric-title {
    color: #2563eb;
}

.metric-card:hover .metric-value {
    color: #0f172a;
}

/* OPTIONAL: subtle glow */
.metric-card:hover {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f8fafc 100%
    );
}
.metric-card {
    background: white;
    border-radius: 22px;
    padding: 20px;
    border: 1px solid #dfe8ec;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    transition: all 0.35s ease;
    cursor: pointer;
}

    .chip {
        display: inline-block;
        margin-bottom: 12px;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.20);
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.03em;
    }

    .metric-card{
    background:#ffffff;
    border:1px solid #d9e5ea;
    border-radius:26px;
    padding:22px;
    box-shadow:
        0 8px 24px rgba(15,23,42,0.05),
        0 2px 6px rgba(15,23,42,0.03);
    min-height:132px;
}

    .metric-title {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .metric-value {
        color: var(--text);
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .metric-sub {
        color: var(--muted);
        font-size: 13px;
    }

    .panel{
    background:white;
    border:1px solid #e2e8f0;
    border-radius:28px;
    padding:18px;
    box-shadow:0 8px 24px rgba(15,23,42,.05);
    height:auto !important;
    min-height:auto !important;
}

.panel:hover{
    transform:translateY(-2px);
    box-shadow:
        0 14px 32px rgba(15,23,42,0.08),
        0 4px 12px rgba(15,23,42,0.05);
}

    .panel-title {
        color: var(--text);
        font-size: 1.05rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .kicker {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 12px;
    }

    .status-good {
        color: var(--green);
        font-weight: 800;
    }

    .status-bad {
        color: var(--red);
        font-weight: 800;
    }

    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .info-box {
        background: #f7fafb;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 14px;
    }

    .info-label {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 4px;
    }

    .info-value {
        color: var(--text);
        font-size: 1rem;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: var(--muted);
        margin-top: 12px;
        font-size: 13px;
        padding-bottom: 10px;
    }

    div[data-testid="stHorizontalBlock"]{
        align-items: stretch !important;
        gap: 16px !important;
    }
    .metric-card:hover,
    .panel:hover{
        transform:translateY(-3px);
        transition:.25s ease;
        box-shadow:0 14px 24px rgba(0,0,0,.07);
    }
    .js-plotly-plot,
.plotly,
svg.main-svg{
    border-radius:18px !important;
}
div[data-testid="stVerticalBlock"]:has(div[data-testid="stPlotlyChart"]) {
    background:white;
    border:1px solid #e2e8f0;
    border-radius:28px;
    padding:18px;
    box-shadow:0 8px 24px rgba(15,23,42,.05);
    height: fit-content !important;
    align-self: start !important;
}

    </style>
    """,
        unsafe_allow_html=True,
    )

    def safe_encode(sample: pd.DataFrame) -> pd.DataFrame:
        sample = sample.copy()
        for col, encoder in encoders.items():
            if col in sample.columns:
                values = sample[col].astype(str)
                known = set(encoder.classes_)
                values = values.apply(lambda x: x if x in known else encoder.classes_[0])
                sample[col] = encoder.transform(values)
        return sample

    def rating_from_roi(roi: float) -> str:
        if roi >= 35:
            return "Strong Buy"
        if roi >= 20:
            return "Buy"
        if roi >= 10:
            return "Hold"
        if roi >= 0:
            return "Cautious"
        return "Avoid"

    def rating_color(rating: str) -> str:
        if rating in {"Strong Buy", "Buy"}:
            return "#16a34a"
        if rating == "Hold":
            return "#d97706"
        if rating == "Cautious":
            return "#ea580c"
        return "#dc2626"

    def get_feature_importance(model, feature_names):
        if hasattr(model, "feature_importances_"):
            imp = pd.DataFrame(
                {"Feature": feature_names, "Importance": model.feature_importances_}
            ).sort_values("Importance", ascending=False)
            return imp.head(8)
        return pd.DataFrame(columns=["Feature", "Importance"])

    
    st.session_state["shared_df"] = filtered.copy()

    if filtered.empty:
        filtered = df[df["City"].astype(str) == selected_city]

    template_row = filtered.iloc[[0]].copy()

    st.sidebar.markdown("### 🏠 Property Details")
    bhk = st.sidebar.slider("BHK", 1, 10, int(template_row["BHK"].iloc[0]))
    sqft = st.sidebar.slider("Area (SqFt)", 300, 6000, int(template_row["Size_in_SqFt"].iloc[0]))
    price = st.sidebar.slider("Current Price (Lakhs)", 10, 500, int(template_row["Price_in_Lakhs"].iloc[0]))
    year = st.sidebar.slider("Year Built", 1990, 2026, int(template_row["Year_Built"].iloc[0]))

    st.sidebar.markdown("### 📍 Location Signals")
    schools = st.sidebar.slider("Nearby Schools", 0, 10, int(pd.to_numeric(template_row["Nearby_Schools"], errors="coerce").fillna(5).iloc[0]))
    hospitals = st.sidebar.slider("Nearby Hospitals", 0, 10, int(pd.to_numeric(template_row["Nearby_Hospitals"], errors="coerce").fillna(5).iloc[0]))
    transport = st.sidebar.slider(
        "Public Transport Accessibility", 1, 10,
        int(pd.to_numeric(template_row["Public_Transport_Accessibility"], errors="coerce").fillna(5).iloc[0]),
    )

    run = st.sidebar.button("🚀 Generate Forecast", type="primary", use_container_width=True)

    st.markdown("""
<div class="hero">
    <div class="chip">Next-Gen Property Insights Platform</div>
    <h1>Real Estate Investment Advisor</h1>
    <p>
        Predict property profitability, estimate 5-year future value,
        and explore city-level real estate insights in one dashboard.
    </p>
</div>
""", unsafe_allow_html=True)

    property_age = 2026 - year
    price_per_bhk = price / max(bhk, 1)

    sample = template_row.copy()
    sample["State"] = selected_state
    sample["City"] = selected_city
    sample["Locality"] = selected_locality
    sample["Property_Type"] = selected_ptype
    sample["BHK"] = bhk
    sample["Size_in_SqFt"] = sqft
    sample["Price_in_Lakhs"] = price
    sample["Year_Built"] = year
    sample["Nearby_Schools"] = schools
    sample["Nearby_Hospitals"] = hospitals
    sample["Public_Transport_Accessibility"] = transport
    sample["Property_Age"] = property_age
    sample["Price_per_BHK"] = price_per_bhk

    sample_encoded = safe_encode(sample)

    sample_encoded["City_Growth"] = 1.08
    sample_encoded["Type_Growth"] = 1.07

    sample_class = sample_encoded[clf.feature_names_in_]
    sample_reg = sample_encoded[reg.feature_names_in_]

    pred_class = 0
    pred_price = float(price)
    confidence = 0.0
    profit = 0.0
    roi = 0.0

    if run:
        pred_class = int(clf.predict(sample_class)[0])
        pred_price = float(reg.predict(sample_reg)[0])
        confidence = float(clf.predict_proba(sample_class)[0].max() * 100)
        profit = pred_price - price
        roi = (profit / price) * 100 if price else 0.0

    investment_label = "Yes" if pred_class == 1 else "No"
    rating = rating_from_roi(roi)
    rating_hex = rating_color(rating)

    m1, m2, m3, m4 = st.columns(4, gap="large")

    st.markdown(f"""
    <script>
    let conf = 0;
    let confTarget = {confidence:.1f};

    let confInterval = setInterval(function(){{
        conf += 1.2;
        if(conf >= confTarget){{
            conf = confTarget;
            clearInterval(confInterval);
        }}
        let el=document.getElementById("conf-box");
        if(el) el.innerHTML = conf.toFixed(1) + "%";
    }},20);
    </script>
    """, unsafe_allow_html=True)

    with m1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Model Prediction</div>
                <div class="metric-value" style="color:{'#16a34a' if pred_class == 1 else '#dc2626'};">{investment_label}</div>
                <div class="metric-sub">ROI-Based Suggestion {rating}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Confidence Score</div>
                <div class="metric-value" id="conf-box">{confidence:.1f}%</div>
                <div class="metric-sub">Classifier certainty for this forecast</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">5-Year Estimated Value</div>
                <div class="metric-value">₹ {pred_price:.1f}L</div>
                <div class="metric-sub">Profit: ₹ {profit:.1f}L · ROI: {roi:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with m4:
        st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Investment Rating</div>
        <div class="metric-value" style="font-size:32px;color:{rating_hex};">{rating}</div>
        <div class="metric-sub">Overall Recommendation</div>
    </div>
    """, unsafe_allow_html=True)    

    c1, c2, c3, c4 = st.columns([1.85,1.35,1.35,1.35], gap="large")

    with c1:

        st.markdown("""
        <div style="
            font-size:18px;
            font-weight:800;
            color:#0f172a;
            margin-bottom:4px;
        ">
            Future Price Trend
        </div>

        <div style="
            font-size:11px;
            color:#64748b;
            margin-bottom:12px;
        ">
            Projected property value movement from 2026 to 2031.
        </div>
        """, unsafe_allow_html=True)

        # =============================
        # 🔥 DATA GENERATION
        # =============================
        years = list(range(2026, 2032))
        values = []

        base_pred = reg.predict(sample_reg)[0]

        for i, yr in enumerate(years):

            # simple realistic growth (SAFE)
            growth_rate = 0.025   # 2.5% yearly

            adjusted_price = base_pred * ((1 + growth_rate) ** i)

            values.append(adjusted_price)

        # =============================
        # 🔥 CREATE FIGURE
        # =============================
        fig_trend = go.Figure()

        fig_trend.add_trace(
            go.Scatter(
                x=years,
                y=values,
                mode="lines+markers",
                line=dict(
                    color="#0f766e",
                    width=4,
                    shape="spline",
                    smoothing=1.2
                ),
                marker=dict(
                    color="#f97316",
                    size=9,
                    line=dict(color="white", width=2)
                )
            )
        )

        # =============================
        # 🔥 CLEAN UI LAYOUT (LIKE IMAGE 2)
        # =============================
        fig_trend.update_layout(
            height=392,
            margin=dict(t=0, l=10, r=10, b=10),

            paper_bgcolor="white",
            plot_bgcolor="white",

            showlegend=False,

            xaxis=dict(
                showgrid=True,
                gridcolor="#e2e8f0",
                griddash="dash",
                showline=True,
                zeroline=True,
                linecolor="#000000",
                tickfont=dict(size=11, color="#000000"),
                
                
                
            ),

            yaxis=dict(
                title="Price (Lakhs)",
                title_font=dict(size=11, color="#000000"),

                showgrid=True,
                gridcolor="#e2e8f0",
                griddash="dot",

                showline=True,
                linecolor="#000000",

                tickfont=dict(size=11, color="#000000"),

                nticks=6   # 🔥 CLEAN AXIS (IMPORTANT)
            ),

            font=dict(
                family="Inter, sans-serif",
                color="#334155"
            )
        )

        # =============================
        # 🔥 RENDER
        # =============================
        st.plotly_chart(fig_trend, use_container_width=True) 

    with c2:

        with st.container():

            # Title
            st.markdown("""
            <div style="
                font-size:18px;
                font-weight:800;
                color:#0f172a;
                margin-bottom:14px;
                background:white;
            ">
                Prediction Snapshot
            </div>
            """, unsafe_allow_html=True)

            # 4 Snapshot Boxes
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">

            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;">Current Price</div>
            <div style="font-size:20px;font-weight:800;color:#0f172a;">₹ {price:.1f}L</div>
            </div>

            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;">Expected Profit</div>
            <div style="font-size:20px;font-weight:800;color:{'#16a34a' if profit >= 0 else '#dc2626'};">₹ {profit:.1f}L</div>
            </div>

            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;">ROI</div>
            <div style="font-size:20px;font-weight:800;color:{'#16a34a' if roi >= 20 else '#dc2626'};">{roi:.1f}%</div>
            </div>

            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:14px;">
            <div style="font-size:12px;color:#94a3b8;">Investment Rating</div>
            <div style="font-size:20px;font-weight:800;color:{rating_hex};">{rating}</div>
            </div>

            </div>
            """, unsafe_allow_html=True)

            # Recommendation Title
            st.markdown("""
            <div style="
                margin-top:18px;
                margin-bottom:10px;
                font-size:16px;
                font-weight:800;
                color:#0f172a;
            ">
                Why This Recommendation?
            </div>
            """, unsafe_allow_html=True)

            # Build Reasons
            reasons = []

            if schools >= 7:
                reasons.append("Strong nearby school ecosystem")

            if hospitals >= 6:
                reasons.append("Good healthcare accessibility")

            if transport >= 6:
                reasons.append("Favorable transport connectivity")

            if property_age <= 10:
                reasons.append("Relatively newer property")

            if roi >= 20:
                reasons.append("Healthy expected ROI outlook")

            if price_per_bhk < 80:
                reasons.append("Balanced pricing per BHK")

            if len(reasons) == 0:
                reasons.append("Neutral market indicators detected")

            # Show Reasons
            for r in reasons:
                st.markdown(
                    f"""
                    <div style="
                        background:#f8fafc;
                        border:1px solid #e2e8f0;
                        border-radius:14px;
                        padding:10px 12px;
                        margin-bottom:8px;
                        font-size:14px;
                        font-weight:600;
                        color:#0f172a;
                    ">
                        ✅ {r}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)
        

    with c3:
        st.markdown('<div class="panel-title">City Price Heatmap</div>', unsafe_allow_html=True)

        city_heat = (
            df.groupby("City", as_index=False)["Price_in_Lakhs"]
            .mean()
            .sort_values("Price_in_Lakhs", ascending=False)
        )

        fig_heat = px.treemap(
            city_heat,
            path=["City"],
            values="Price_in_Lakhs",
            color="Price_in_Lakhs",
            color_continuous_scale=[
                [0.0,  "#00f5d4"],
                [0.3,  "#00c9a7"],   # mid teal
                [0.6,  "#0077b6"],   # medium blue
                [0.8,  "#023e8a"],   # dark blue
                [1.0,  "#03045e"],
            ]
        )

        fig_heat.update_traces(
            texttemplate="<b>%{label}</b><br>%{value:.2f} L",
            textinfo="label",
            textfont_size=11,
            marker_line_width=1,
            marker_line_color="white"
        )

        fig_heat.update_layout(
            height=410,
            margin=dict(t=10, l=10, r=10, b=100),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(
                family="Inter, sans-serif",
                size=11,
                color="#0f172a"
            ),
            coloraxis_colorbar=dict(
                title=dict(
                    text="Price (Lakhs)",
                    side="bottom",
                    font=dict(color="#0f172a")
                ),
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.28,
                thickness=12,
                len=1.1,
                tickformat=".1f",
                tickfont=dict(size=10, color="#0f172a"),
            )
        )

        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        import numpy as np

    with c4:
        st.markdown('<div class="panel-title">Area vs Price Correlation</div>', unsafe_allow_html=True)

        corr_df = df[df["City"].astype(str) == selected_city].copy()

        # Add jitter to spread dots
        np.random.seed(42)
        corr_df["Size_jitter"] = corr_df["Size_in_SqFt"] + np.random.uniform(
            -100, 100, size=len(corr_df)
        )
        corr_df["Price_jitter"] = corr_df["Price_in_Lakhs"] + np.random.uniform(
            -5, 5, size=len(corr_df)
        )

        fig_corr = px.scatter(
            corr_df,
            x="Size_jitter",
            y="Price_jitter",
            labels={
                "Size_jitter": "Size (in SqFt)",
                "Price_jitter": "Price (Lakhs)"
            }
        )

        fig_corr.update_traces(
            marker=dict(
                size=8,
                opacity=0.99,
                color="#7b9dd4",
                line=dict(
                    width=0.5,
                    color="#5679c4"
                )
            )
        )

        fig_corr.update_layout(
            height=400,
            margin=dict(t=8, l=8, r=8, b=8),
            paper_bgcolor="white",
            plot_bgcolor="white",
            coloraxis_showscale=False,
            font=dict(color="#334155", family="Inter, sans-serif", size=11),
            xaxis=dict(
                title="Size (in SqFt)",
                showgrid=True,
                gridcolor="rgba(200,210,230,0.4)",
                gridwidth=1,
                griddash="dash",
                zeroline=True,
                tickfont=dict(size=10, color="#000000"),
                title_font=dict(size=11, color="#000000"),
            ),
            yaxis=dict(
                title="Price (Lakhs)",
                showgrid=True,
                gridcolor="rgba(200,210,230,0.4)",
                gridwidth=1,
                griddash="dash",
                zeroline=True,
                tickfont=dict(size=10, color="#000000"),
                title_font=dict(size=11, color="#000000"),
            ),
        )

        st.plotly_chart(fig_corr, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4, gap="large")

    with r1:
        st.markdown('<div class="panel-title">Average Price by City</div>', unsafe_allow_html=True)

        city_rank = (
            df.groupby("City", as_index=False)["Price_in_Lakhs"]
            .mean()
            .sort_values("Price_in_Lakhs", ascending=False)
            .head(10)
        )

        bar_colors = [
            "#2f5d73",  # Bangalore
            "#35697a",  # Surat
            "#4b8b8b",  # Kochi
            "#6fa8a3",  # Gaya
            "#7fb3ad",  # Mangalore
            "#8dbbb5",  # Dehradun
            "#98c4be",  # Mysore
            "#9fc9c3",  # Chennai
            "#abd3cd",  # Hyderabad
            "#bfe4dd",  # Coimbatore
        ]

        fig_city = px.bar(
            city_rank,
            x="City",
            y="Price_in_Lakhs"
        )

        fig_city.update_traces(
            marker_color=bar_colors,
            marker_line_width=0,
            width=0.78
        )

        fig_city.update_layout(
            height=400,
            margin=dict(t=8,l=10,r=8,b=8),

            paper_bgcolor="white",
            plot_bgcolor="white",

            coloraxis_showscale=False,
            showlegend=False,

            font=dict(
                family="Inter, sans-serif",
                color="#64748b",
                size=12
            ),

            xaxis=dict(
                title="",
                tickangle=-38,
                showgrid=True,
                showline=True,
                linewidth=1,
                tickfont=dict(size=10, color="#000000"),
                linecolor="#000000"
            ),

            yaxis=dict(
                title="",
                title_font=dict(size=9, color="#94a3b8"),
                title_standoff=139,
                automargin=False,
                range=[0,260],
                dtick=65,
                showgrid=True,
                gridcolor="#dbe3f0",
                griddash="dash",
                zeroline=True,
                showline=True,
                linewidth=1,
                tickfont=dict(size=10, color="#000000"),
                linecolor="#000000"
            )
        )

        st.plotly_chart(fig_city, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="panel-title">Property Type Mix</div>', unsafe_allow_html=True)

        type_mix = df["Property_Type"].astype(str).value_counts().head(6).reset_index()
        type_mix.columns = ["Property_Type", "Count"]

        fig_donut = px.pie(
        type_mix,
        names="Property_Type",
        values="Count",
        hole=0.62,
        color="Property_Type",
        color_discrete_map={
            "Villa": "#157a72",
            "Independent House": "#2f63db",
            "Apartment": "#f25c05"
        }
    )

        fig_donut.update_traces(
        sort=False,
        domain=dict(x=[0.12,0.88], y=[0.22,0.95]),
        textinfo="percent",
        textposition="outside",
        textfont=dict(size=16),
        marker=dict(
            line=dict(color="white", width=4)
        )
    )

        fig_donut.update_layout(
        height=400,
        margin=dict(t=8,l=8,r=8,b=8),

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Inter, sans-serif",
            color="#334155"
        ),

        showlegend=True,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11, color="#000000"),
            traceorder="normal"
        )
    )

        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r3:
        st.markdown('<div class="panel-title">Feature Importance</div>', unsafe_allow_html=True)

        importance_df = get_feature_importance(clf, clf.feature_names_in_)

        if not importance_df.empty:
            importance_df = importance_df.sort_values("Importance", ascending=False).reset_index(drop=True)

            bar_colors = [
                "#3f66d9",
                "#4d6fd9",
                "#6077d7",
                "#6d7bd8",
                "#7c7ed7",
                "#8b83d8",
                "#9b89d8",
                "#ab8fda",
            ]

            fig_imp = px.bar(
                importance_df,
                x="Importance",
                y="Feature",
                orientation="h",
            )

            fig_imp.update_traces(
                marker_color=bar_colors[:len(importance_df)],
                marker_line_width=0,
                width=0.80,
                marker=dict(cornerradius=8)
            )

            fig_imp.update_layout(
                height=400,
                margin=dict(t=20, l=5, r=15, b=60),
                paper_bgcolor="white",
                plot_bgcolor="white",
                showlegend=False,
                xaxis_title="Importance",
                yaxis_title="",
                font=dict(color="#667085"),
                bargap=0.26,
            )

            fig_imp.update_xaxes(
                domain=[0.32, 1.0],
                range=[0, 0.22],
                tickvals=[0.00, 0.06, 0.11, 0.17, 0.22],
                tickformat=".2f",
                showgrid=True,
                gridcolor="#d9dee7",
                gridwidth=1,
                zeroline=False,
                showline=True,
                linecolor="#6b7280",
                linewidth=1.4,
                tickfont=dict(size=11, color="#000000"),
                title_font=dict(size=11, color="#000000")
            )

            fig_imp.update_yaxes(
                autorange="reversed",
                automargin=False,
                showgrid=False,
                showline=True,
                linecolor="#6b7280",
                linewidth=1.4,
                tickfont=dict(size=11, color="#000000")
            )

            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.info("Feature importance is unavailable for this model.")

        with r4:
            st.markdown('<div class="panel-title">Model Metrics Panel</div>', unsafe_allow_html=True)

            if str(investment_label).strip().lower() == "yes":
                class_color = "#16a34a"   # green
            elif str(investment_label).strip().lower() == "no":
                class_color = "#dc2626"   # red
            else:
                class_color = "#1f2937"   # default dark
                
            st.markdown(
                f"""
                <style>
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 14px 18px;
                    margin-top: 6px;
                    margin-bottom: 14px;
                }}
                .info-box {{
                    background: #ffffff;
                    border: 1.4px solid #d7dee7;
                    border-radius: 18px;
                    padding: 10px 14px;
                    min-height: 64px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }}
                .info-label {{
                    font-size: 11px;
                    font-weight: 500;
                    color: #6b7280;
                    margin-bottom: 6px;
                }}
                .info-value {{
                    font-size: 15px;
                    font-weight: 800;
                    color: #1f2937;
                    line-height: 1.08;
                }}
                </style>

                <div class="info-grid">
                    <div class="info-box">
                        <div class="info-label">Classification Output</div>
                        <div class="info-value" style="color:{class_color};">{investment_label}</div>
                    </div>
                    <div class="info-box">
                        <div class="info-label">Confidence</div>
                        <div class="info-value">{confidence:.1f}%</div>
                    </div>
                    <div class="info-box">
                        <div class="info-label">5Y Forecast</div>
                        <div class="info-value">₹ {pred_price:.1f}L</div>
                    </div>
                    <div class="info-box">
                        <div class="info-label">ROI Outlook</div>
                        <div class="info-value" style="color:{class_color};">{roi:.1f}%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
                )

            locality_avg = (
                df.loc[df["City"].astype(str) == selected_city]
                .groupby("Locality", as_index=False)["Price_in_Lakhs"]
                .mean()
                .sort_values("Price_in_Lakhs", ascending=True)
                .tail(8)
                .reset_index(drop=True)
            )

            bar_colors = [
                "#eadb8b",
                "#e8cf74",
                "#e8c561",
                "#e7bd56",
                "#e6b54a",
                "#e5ab42",
                "#df742d",
                "#da6528",
            ]

            fig_locality = px.bar(
                locality_avg,
                x="Price_in_Lakhs",
                y="Locality",
                orientation="h",
            )

            fig_locality.update_traces(
                marker_color=bar_colors[:len(locality_avg)],
                marker_line_width=0,
                width=0.54
            )

            fig_locality.update_layout(
                height=255,
                margin=dict(t=0, l=92, r=30, b=34),
                paper_bgcolor="white",
                plot_bgcolor="white",
                showlegend=False,
                bargap=0.34,
                xaxis_title="Avg Price (Lakhs)",
                yaxis_title="",
                font=dict(color="#000000")
            )

            fig_locality.update_xaxes(
                range=[0, max(380, locality_avg["Price_in_Lakhs"].max() * 1.02)],
                tickvals=[0, 100, 200, 300],
                showgrid=False,
                zeroline=True,
                showline=True,
                tickfont=dict(size=11, color="#000000"),
                title_font=dict(size=11, color="#000000")
            )

            fig_locality.update_yaxes(
                autorange="reversed",
                showgrid=False,
                showline=True,
                tickfont=dict(size=11, color="#000000")
            )

            st.plotly_chart(fig_locality, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # PDF REPORT
    # =========================
    def create_pdf():

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)

        pdf.cell(200, 10, txt="Real Estate Investment Report", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=11)

        lines = [
            f"State: {selected_state}",
            f"City: {selected_city}",
            f"Locality: {selected_locality}",
            f"Property Type: {selected_ptype}",
            f"BHK: {bhk}",
            f"Area: {sqft} SqFt",
            f"Current Price: Rs {price:.1f} Lakhs",
            f"Good Investment: {investment_label}",
            f"Confidence: {confidence:.1f}%",
            f"Future Price: Rs {pred_price:.1f} Lakhs",
            f"Profit: Rs {profit:.1f} Lakhs",
            f"ROI: {roi:.1f}%",
            f"Rating: {rating}",
        ]

        for line in lines:
            pdf.cell(200, 8, txt=line, ln=True)

        # 🔥 IMPORTANT FIX
        return pdf.output(dest="S").encode("latin-1")
    pdf_bytes = create_pdf()
   
    col1, col2, col3 = st.columns([1, 1, 1])  # adjust ratio
    st.download_button(
    label="⤓Download",
    data=pdf_bytes,
    file_name="investment_report.pdf",
    mime="application/pdf",
    use_container_width=False   # 👈 IMPORTANT
)

    # components.html(f"""
    # <a onclick="
    #     var a=document.createElement('a');
    #     a.href='data:application/pdf;base64,{pdf_b64}';
    #     a.download='investment_report.pdf';
    #     a.click();
    # " style="
    #     position:fixed;top:17px;right:22px;z-index:99999;
    #     display:flex;align-items:center;height:44px;padding:0 22px;
    #     border-radius:12px;background:#1d4ed8;color:white;
    #     font-weight:700;font-size:14px;text-decoration:none;
    #     border:1px solid rgba(255,255,255,.12);cursor:pointer;">
    #     &#8595; Download
    # </a>
    # """, height=0)

    st.markdown(
            """
        <div class="footer">
            Real Estate Investment Advisor | Streamlit Dashboard
        </div>
        """,
            unsafe_allow_html=True,
        )

elif selected == "EDA Insights":
    import eda
    eda.run(df)