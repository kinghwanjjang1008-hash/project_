import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Population Analysis", layout="wide")

st.title("📊 서울시 행정구역별 연령대별 인구 분포 분석")
st.markdown("공공데이터 기반 행정구역별 인구수 꺾은선 그래프 시각화 앱입니다.")

@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        if col != "행정구역":
            df[col] = df[col].astype(str).str.replace(",", "", regex=False)
            df[col] = df[col].astype(str).str.replace('"', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

try:
    df = load_data()

    st.sidebar.header("🔍 Select Region")
    region_list = df["행정구역"].unique().tolist()
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", region_list)

    region_data = df[df["행정구역"] == selected_region].iloc[0]

    age_columns = ["67", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    display_age_labels = ["0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]

    population_values = []
    for col in age_columns:
        population_values.append(int(region_data[col]))

    rainbow_colors = [
        '#FF0000', '#FF7F00', '#FFD700', '#00FF00', '#0000FF', 
        '#4B0082', '#8B00FF', '#FF1493', '#FF00FF', '#00FFFF', '#8B4513'
    ]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=display_age_labels,
        y=population_values,
        mode='lines+markers+text',
        text=[f"{x:,}" for x in population_values],
        textposition="top center",
        line=dict(width=3, color='#888888'),
        marker=dict(
            size=14,
            color=rainbow_colors,
            line=dict(width=2, color='white')
        ),
        name="Population"
    ))

    fig.update_layout(
        title=f"<b>{selected_region} 연령대별 인구수</b>",
        xaxis_title="연령대 (나이)",
        yaxis_title="인구수 (명)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=600,
        xaxis=dict(
            showgrid=True, 
            gridcolor='#EAEAEA',
            linecolor='#111111', 
            linewidth=1
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='#EAEAEA',
            linecolor='#111111', 
            linewidth=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 상세 데이터")
    table_df = pd.DataFrame([population_values], columns=display_age_labels, index=["인구수 (명)"])
    st.dataframe(table_df, use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
