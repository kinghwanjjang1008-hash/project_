import streamlit as st
import pandas as pd
import plotly.graph_objects as px

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

    # 연령대 컬럼 정의 (불필요한 총인구수 컬럼 제외)
    # 원본의 '67' 컬럼은 직관적인 이해를 위해 '0~9세'로 변경하여 표시합니다.
    age_columns = ["67", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    display_age_labels = ["0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]

    population_values = [region_data[col] for col in age_columns]

    # 그래프를 위한 데이터프레임 생성
    plot_df = pd.DataFrame({
        "연령대": display_age_labels,
        "인구수": population_values
    })

    # 5. 무지개색 꺾은선 그래프 생성 (Plotly)
    # 연령대별로 선의 색상이 무지개색 그라데이션으로 이어지도록 표현
    rainbow_colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#8B00FF', '#FF007F', '#FF00FF', '#7F00FF', '#00FFFF']
    
    fig = px.figure()
    
    # 꺾은선(Line) 추가 (바탕은 흰색, 선과 마커에 무지개색 그라데이션 효과를 주기 위해 선 요소를 세부 설정)
    fig.add_trace(px.scatter(
        plot_df, 
        x="연령대", 
        y="인구수",
