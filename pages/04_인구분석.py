import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Population Analysis", layout="wide")

st.title("📊 서울시 행정구역 및 연령대별 인구 분석 앱")
st.markdown("공공데이터 기반으로 행정구역별 인구 분포 및 연령대별 최다 인구 지역을 분석합니다.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("population.csv", encoding="cp949")
    except:
        df = pd.read_csv("population.csv", encoding="euc-kr")
        
    df.columns = df.columns.str.strip()
    
    for col in df.columns:
        if col != "행정구역":
            df[col] = df[col].astype(str).str.replace(",", "", regex=False)
            df[col] = df[col].astype(str).str.replace('"', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

try:
    df = load_data()

    # 사이드바에서 분석 모드 선택하도록 구성
    st.sidebar.header("⚙️ 분석 모드 선택")
    mode = st.sidebar.radio("원하는 분석을 선택하세요", ["행정구역별 분석", "연령대별 최다 지역 분석"])

    # 원본 파일 컬럼명 리스트와 화면 표시용 레이블 리스트 정의
    age_columns = ["67", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    display_age_labels = ["0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세", "60~69세", "70~79세", "80~89세", "90~99세", "100세 이상"]
    
    # 컬럼명 매핑 딕셔너리 (화면 표시용 -> 원본 데이터용)
    age_map = dict(zip(display_age_labels, age_columns))

    # 무지개 색상 팔레트 (최대 25개 자치구를 커버하기 위해 넉넉하게 확장된 무지개 컬러 패턴)
    rainbow_colors = [
        '#FF0000', '#FF4500', '#FF7F00', '#FFA500', '#FFD700', 
        '#FFFF00', '#ADFF2F', '#7FFF00', '#00FF00', '#00FF7F', 
        '#00FFFF', '#00BFFF', '#0000FF', '#4B0082', '#8B00FF', 
        '#9400D3', '#C71585', '#FF1493', '#FF00FF', '#FF69B4',
        '#FA8072', '#FF6347', '#EE82EE', '#8A2BE2', '#4169E1'
    ]

    if mode == "행정구역별 분석":
        st.sidebar.subheader("🔍 행정구역 선택")
        region_list = df["행정구역"].unique().tolist()
        selected_region = st.sidebar.selectbox("행정구역을 선택하세요", region_list)

        region_data = df[df["행정구역"] == selected_region].iloc[0]

        population_values = []
        for col in age_columns:
            population_values.append(int(region_data[col]))

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
                color=rainbow_colors[:len(display_age_labels)],
                line=dict(width=2, color='white')
            ),
            name="인구수"
        ))

        fig.update_layout(
            title=f"<b>{selected_region} 연령대별 인구수</b>",
            xaxis_title="연령대 (나이)",
            yaxis_title="인구수 (명)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=600,
            xaxis=dict(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111', linewidth=1),
            yaxis=dict(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111', linewidth=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 상세 데이터")
        table_df = pd.DataFrame([population_values], columns=display_age_labels, index=["인구수 (명)"])
        st.dataframe(table_df, use_container_width=True)

    elif mode == "연령대별 최다 지역 분석":
        st.sidebar.subheader("🔍 연령대 선택")
        selected_age_display = st.sidebar.selectbox("분석할 연령대를 선택하세요", display_age_labels)
        
        # 선택한 연령대에 해당하는 실제 파일 내 컬럼명 추출
        target_col = age_map[selected_age_display]

        # '서울특별시' 전체 합계 행은 제외하고 자치구만 추출하여 인구순 정렬
        sub_df = df[df["행정구역"].str.contains("구")].copy()
        sub_df = sub_df.sort_values(by=target_col, ascending=False)

        # 그래프에 그릴 데이터 추출
        regions = sub_df["행정구역"].tolist()
        values = sub_df[target_col].tolist()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=regions,
            y=values,
            mode='lines+markers+text',
            text=[f"{x:,}" for x in values],
            textposition="top center",
            line=dict(width=3, color='#888888'),
            marker=dict(
                size=12,
                color=rainbow_colors[:len(regions)], # 자치구별로 무지개 그라데이션 적용
                line=dict(width=1, color='white')
            ),
            name="인구수"
        ))

        fig.update_layout(
            title=f"<b>{selected_age_display} 인구가 가장 많은 행정구역 순위</b>",
            xaxis_title="행정구역 (구)",
            yaxis_title="인구수 (명)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            height=650,
            xaxis=dict(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111', linewidth=1, tickangle=45),
            yaxis=dict(showgrid=True, gridcolor='#EAEAEA', linecolor='#111111', linewidth=1)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 순위별 상세 데이터")
        rank_df = pd.DataFrame({
            "순위": range(1, len(regions) + 1),
            "행정구역": regions,
            f"{selected_age_display} 인구수 (명)": values
        })
        st.dataframe(rank_df.set_index("순위"), use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
