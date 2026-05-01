import streamlit as st
import base64
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"


def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def apply_global_theme(image_name="sidebar_bg.png"):
    img_path = ASSETS / image_name
    img64 = get_base64(img_path) if img_path.exists() else ""

    st.markdown(f"""
    <style>

    html, body, [class*="css"] {{
        font-family: Inter, Arial, sans-serif;
    }}

    .stApp {{
        background:#eef3f4;
    }}

    .block-container {{
        max-width:1600px;
        padding-top:1.2rem;
        padding-left:1.5rem;
        padding-right:1.5rem;
        padding-bottom:2rem;
    }}

    section[data-testid="stSidebar"] {{
        min-width:320px !important;
        max-width:320px !important;
        border-right:1px solid rgba(255,255,255,0.06);
    }}

    section[data-testid="stSidebar"] > div:first-child {{
        background:
        linear-gradient(rgba(5,8,35,.22), rgba(5,8,35,.45)),
        url("data:image/png;base64,{img64}");
        background-size:cover;
        background-position:center top;
        background-repeat:no-repeat;
    }}

    section[data-testid="stSidebar"] .block-container {{
        background:transparent !important;
        padding-top:1rem;
    }}

    section[data-testid="stSidebar"] * {{
        color:white !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stSlider,
    section[data-testid="stSidebar"] .stButton,
    section[data-testid="stSidebar"] .stNumberInput {{
        background:rgba(255,255,255,.05);
        border:1px solid rgba(255,255,255,.08);
        border-radius:16px;
        padding:8px;
        backdrop-filter:blur(8px);
        margin-bottom:10px;
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        width:100%;
        border:none;
        border-radius:14px;
        color:white;
        font-weight:700;
        background:linear-gradient(135deg,#0f766e,#2563eb);
    }}

    footer {{
        visibility:hidden;
    }}

    </style>
    """, unsafe_allow_html=True)


# def render_sidebar_brand():
#     st.sidebar.markdown("""
#     <div style="
#     padding:18px;
#     border-radius:20px;
#     margin-bottom:18px;
#     background:linear-gradient(135deg,#0f766e,#2563eb);
#     box-shadow:0 14px 28px rgba(37,99,235,.25);
#     ">
#         <div style="font-size:32px;">👑</div>
#         <div style="font-size:28px;font-weight:800;">RealEstate Pro AI</div>
#         <div style="font-size:13px;opacity:.9;">
#         Analytics Intelligence Platform
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

def render_sidebar_brand():
    st.sidebar.markdown("""
    <div style="
    padding:18px;
    border-radius:20px;
    margin-bottom:18px;
    background:linear-gradient(135deg,#0f766e,#2563eb);
    box-shadow:0 14px 28px rgba(37,99,235,.25);
    ">
        <div style="font-size:30px;">🏙️</div>

        <div style="
        font-size:22px;
        font-weight:800;
        line-height:1.25;
        margin-top:8px;
        ">
        Real Estate Investment Advisor
        </div>

        <div style="
        font-size:12px;
        opacity:.92;
        margin-top:8px;
        line-height:1.4;
        ">
        Predicting Property Profitability & Future Value
        </div>
    </div>
    """, unsafe_allow_html=True)