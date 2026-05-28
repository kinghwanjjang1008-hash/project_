import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

# [체크 1] 스트림릿 웹페이지 기본 설정 최적화 및 레이아웃 설정
st.set_page_config(page_title="글로벌 MBTI 데이터 분석기", layout="centered")

st.title("🌏 전 세계 MBTI 데이터 분석기")
st.markdown("원하는 분석 탭을 선택하여 국가별 또는 MBTI 유형별 데이터를 확인해 보세요.")

# [체크 2] 데이터 캐싱 처리로 대용량 조회 시 앱 속도 저하 방지
@st.cache_data
def load_data():
    try:
        # 파일 경로가 메인 디렉토리에 있을 때 안전하게 로드
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        return None

df = load_data()

# [체크 3] 데이터 로드 실패 시 예외 처리 보강
if df is None:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 파일이 프로젝트 최상위 폴더(Root)에 업로드되어 있는지 확인해 주세요.")
else:
    # [체크 4] 데이터 컬럼 유효성 검사 (첫 열은 Country, 이후 16개는 MBTI 유형이어야 함)
    all_mbti_types = df.columns[1:].tolist()
    country_list = sorted(df['Country'].dropna().unique())

    # 탭 구성으로 사용자 UI 편의성 극대화
    tab1, tab2 = st.tabs(["📍 국가별 MBTI 비율", "📊 MBTI별 상위 국가 TOP 10"])

    # ----------------------------------------------------------------
    # TAB 1: 국가별 MBTI 비율 분석
    # ----------------------------------------------------------------
    with tab1:
        st.subheader("📌 국가별 MBTI 성향 확인")
        selected_country = st.selectbox("👉 분석할 국가를 선택하세요:", country_list, key="sb_country")

        # [체크 5] 선택된 국가 데이터 추출 시 안전한 .iloc 슬라이싱 처리
        country_rows = df[df['Country'] == selected_country]
        
        if not country_rows.empty:
            country_data = country_rows.iloc[0, 1:]
            # 비율 기준 내림차순 정렬 (높은 순)
            country_data = country_data.sort_values(ascending=False)

            mbti_types_c = country_data.index.tolist()
            # [체크 6] 원본 데이터가 소수점(예: 0.1188)일 때를 대비해 % 수치로 안전하게 변환
            percentages_c = [float(val) * 100 if float(val) <= 1.0 else float(val) for val in country_data.values]

            # [체크 7] 1등 Crimson 고정 및 2등 이하 순위별 빨->주->노->초 그라데이션 자동 연산
            colors_c = []
            num_items_c = len(mbti_types_c)
            cmap_c = mcolors.LinearSegmentedColormap.from_list("grad_c", ["#FF3333", "#FF9933", "#FFFF66", "#99FF99", "#E6FFE6"])
            
            for i in range(num_items_c):
                if i == 0:
                    colors_c.append("crimson") 
                else:
                    idx = (i - 1) / (num_items_c - 2) if num_items_c > 2 else 0.5
                    colors_c.append(mcolors.to_hex(cmap_c(idx)))

            # Plotly 막대그래프 시각화
            fig_c = go.Figure()
            fig_c.add_trace(go.Bar(
                x=mbti_types_c, 
                y=percentages_c,
                marker=dict(color=colors_c, line=dict(color='#333333', width=1)),
                text=[f"{p:.2f}%" for p in percentages_c], 
                textposition='auto'
            ))
            
            # 1등 막대 위에 🌈 1위 하이라이트 Annotation 표시
            fig_c.add_annotation(
                x=mbti_types_c[0], y=percentages_c[0], text="🌈 1위",
                showarrow=True, arrowhead=2, ax=0, ay=-30, 
                font=dict(size=13, color="black", family
