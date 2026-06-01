import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 기본 설정
st.set_page_config(page_title="서울시 인구 분석", layout="wide")

st.title("서울시 행정구역별 연령대별 인구 분포 분석")
st.markdown("업로드된 population.csv 데이터를 바탕으로 꺾은선 그래프를 그립니다.")

@st.cache_data
def load_data():
    # 데이터 로드 및 정제
    df = pd.read_csv("population.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    
    # 숫자 데이터 전처리
    for col in df.columns:
        if col != "행정구역":
            df[col] = df[col].astype(str).str.replace(",", "")
            df[col] = df[col].astype(str).str.replace('"', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

try:
    df = load_data()

    # 사이드바 선택
    st.sidebar.header("조건 선택")
    region_list = df["행정구역"].unique().tolist()
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", region_list)

    # 데이터 추출
    region_data = df[df["행정구역"] == selected_region].iloc[0]

    # 원본 컬럼명과 매칭할 레이블 정의
    age_columns = ["67", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    display_age_labels = ["0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]

    population_values = []
    for col in age_columns:
        population_values.append(int(region_data[col]))

    # 무지개 색상 정의 (요청하신 꺾은선 포인트 색상)
    rainbow_colors = [
        '#FF0000', '#FF7F00', '#FFD700', '#00FF00', '#0000FF', 
        '#4B0082', '#8B00FF', '#FF1493', '#FF00FF', '#00FFFF', '#8B4513'
    ]

    # 그래프 생성
    fig = go.Figure()

    # 꺾은선 데이터 추가
    fig.add_trace(go.Scatter(
        x=display_age_labels,
        y=population_values,
        mode='lines+markers+text',
        text=population_values,
        textposition="top center",
        line=dict(width=3, color='#888888'),
        marker=dict(
            size=14,
            color=rainbow_colors,
            line=dict(width=2, color='white')
        ),
        name="인구수"
    ))

    # 레이아웃 설정 (흰색 바탕 및 격자 설정)
    fig.update_layout(
        title="행정구역 연령대별 인구수 꺾은선 그래프",
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
        yaxis=
