import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 기본 설정 (바탕화면 흰색을 위한 기본 테마 적용)
st.set_page_config(page_title="서울시 연령별 인구 분석", layout="wide")

st.title("📊 서울시 행정구역별 연령대별 인구 분포 분석")
st.markdown("업로드된 `population.csv` 데이터를 바탕으로 행정구역별 인구 꺾은선 그래프를 그립니다.")

# 2. 데이터 불러오기 함수
@st.cache_data
def load_data():
    # CSV 파일 읽기 (인구수 데이터의 쉼표 제거 및 숫자 변환)
    df = pd.read_csv("population.csv", encoding="utf-8")
    
    # 컬럼명에 있는 공백 제거
    df.columns = df.columns.str.strip()
    
    # 쉼표(,)가 포함된 문자열 숫자를 정수형으로 변환
    for col in df.columns:
        if col not in ["행정구역"]:
            df[col] = df[col].astype(str).str.replace(",", "").str.replace('"', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    return df

try:
    df = load_data()

    # 3. 사이드바 - 행정구역(구) 선택
    st.sidebar.header("🔍 조건 선택")
    region_list = df["행정구역"].unique().tolist()
    selected_region = st.sidebar.selectbox("행정구역을 선택하세요", region_list)

    # 4. 선택된 행정구역의 데이터 추출 및 정제
    region_data = df[df["행정구역"] == selected_region].iloc[0]

    # 원본 파일의 컬럼명과 매칭할 리스트
    age_columns = ["67", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    # 그래프 가로축(X축)에 이쁘게 보여줄 레이블 리스트
    display_age_labels = ["0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]

    population_values = [int(region_data[col]) for col in age_columns]

    # 5. 무지개색 꺾은선 그래프 생성 (go.Figure로 문법 오류 완벽 해결)
    # 각 포인트(점)에 들어갈 무지개 색상 (빨주노초파남보+핑크+변형색 조합)
    rainbow_colors = [
        '#FF0000', '#FF7F00', '#FFD700', '#00FF00', '#0000FF', 
        '#4B0082', '#8B00FF', '#FF1493', '#FF00FF', '#00FFFF', '#8B4513'
    ]
    
    # 기본 그래프 객체 선언
    fig = go.Figure()
    
    # 하나의 선으로 잇되, 각 포인트 마커에 무지개 색상을 부여
    fig.add_trace(go.Scatter(
        x=display_age_labels,
        y=population_values,
        mode='lines+markers+text',
        text=[f"{val:,}명" for val in population_values],  # 점 위에 인구수 표시 (천단위 쉼표)
        textposition="top center",
        line=dict(width=3, color='#888888'),  # 연결선은 깔끔하고 세련된 그레이 톤
        marker=dict(
            size=14,
            color=rainbow_colors,  # 개별 마커에 무지개 색상 적용
            line=dict(width=2, color='white')  # 테두리를 흰색으로 주어 선명하게
        ),
        name="인구수"
    ))

    # 6. 레이아웃 설정 (흰색 바탕 및 격자 설정)
    fig.update_layout(
        title=dict(
            text=f"<b>[{selected_region}] 연령대별 인구수 꺾은선 그래프</b>", 
            font=dict(size=22, color='#111111'),
            x=0.01
        ),
        xaxis_title="연령대 (나이)",
        yaxis_title
