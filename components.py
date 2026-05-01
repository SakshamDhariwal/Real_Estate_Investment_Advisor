import streamlit as st


def render_navbar(title="Real Estate Advisor", right_text="AI Powered"):
    st.markdown(f"""
    <div style="
    background:#0e1117;
    padding:12px 18px;
    border-radius:16px;
    margin-bottom:18px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">
        <div style="font-size:20px;font-weight:800;color:white;">
            {title}
        </div>
        <div style="font-size:13px;color:#cbd5e1;">
            {right_text}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(title, subtitle, badge="Insights Suite"):
    st.markdown(f"""
    <div style="
    padding:30px 32px;
    border-radius:26px;
    margin-bottom:18px;
    background:linear-gradient(135deg,#0f766e,#2563eb);
    color:white;
    ">
        <div style="
        display:inline-block;
        background:rgba(255,255,255,.15);
        padding:6px 14px;
        border-radius:999px;
        font-size:13px;
        font-weight:600;
        margin-bottom:12px;
        ">
            {badge}
        </div>

        <h1 style="margin:0;font-size:42px;font-weight:800;">
            {title}
        </h1>

        <p style="margin-top:10px;font-size:16px;opacity:.92;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_row(items):
    cols = st.columns(len(items))

    for col, item in zip(cols, items):
        with col:
            st.markdown(f"""
            <div style="
            background:white;
            border-radius:22px;
            padding:20px;
            border:1px solid #dfe8ec;
            box-shadow:0 6px 18px rgba(0,0,0,.04);
            ">
                <div style="font-size:14px;color:#6b7280;">
                    {item['title']}
                </div>

                <div style="
                font-size:34px;
                font-weight:800;
                color:#142230;
                margin-top:6px;
                ">
                    {item['value']}
                </div>

                <div style="font-size:13px;color:#7b8794;">
                    {item.get('sub', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)


def section_title(text):
    st.markdown(f"""
    <div style="
    font-size:24px;
    font-weight:800;
    color:#162330;
    margin:10px 0 14px 0;
    ">
        {text}
    </div>
    """, unsafe_allow_html=True)


def chart_card_open(title="Chart"):
    st.markdown(f"""
    <div style="
    background:white;
    padding:18px;
    border-radius:22px;
    border:1px solid #dfe8ec;
    box-shadow:0 6px 18px rgba(0,0,0,.04);
    margin-bottom:18px;
    ">
        <div style="
        font-size:20px;
        font-weight:800;
        color:#162330;
        margin-bottom:8px;
        ">
            {title}
        </div>
    """, unsafe_allow_html=True)


def chart_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def export_csv(df, filename="report.csv"):
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )