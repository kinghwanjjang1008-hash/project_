import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors
import numpy as np

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 비율 시각화", layout="centered")

st.title("🌏 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 해당 국가의 MBTI 16가지 유형 비율을 확인하실 수 있습니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    # CSV 파일을 읽어옵니다. (동일 디렉토리 기준)
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()

    # 국가 선택 사이드바
    country_list = sorted(df['Country'].unique())
    selected_country = st.selectbox("👉 국가를 선택하세요:", country_list)

    # 선택된 국가의 데이터 추출 및 정렬
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    # 비율이 높은 순서대로 정렬 (상위 데이터가 그래프 위나 왼쪽에 오도록)
    country_data = country_data.sort_values(ascending=False)

    mbti_types = country_data.index.tolist()
    percentages = (country_data.values * 100).tolist() # 백분율(%)로 변환

    # --- 색상 그라데이션 생성 생성 ---
    # 1등: 무지개색 (Plotly의 고유 스타일 패턴을 위해 각 바별 설정 대신, 1등에게 텍스트나 특별 마커를 주거나 여러 색을 혼합할 수 있지만, 
    # 단일 바에 무지개 그라데이션을 넣기 위해 내부 color scale을 활용합니다.)
    
    colors = []
    num_items = len(mbti_types)
    
    # 빨강 -> 주황 -> 노랑 -> 초록 순으로 흐려지는(연해지는) 그라데이션 컬러맵 정의
    # 흐려지도록 끝에 화이트(White)에 가까운 색 배합
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_grad", ["#FF3333", "#FF9933", "#FFFF66", "#99FF99", "#E6FFE6"])
    
    for i in range(num_items):
        if i == 0:
            # 1등 자리는 무지개색 텍스트 효과나 독보적인 멀티컬러를 주지만, 
            # 단일 요소 색상으로 가장 눈에 띄는 '강렬한 무지개빛(자주/네온)' 혹은 완전 차별화된 멀티톤 대용 색상 지정
            colors.append("crimson") 
        else:
            # 2등부터 마지막 등수까지 순서대로 빨->주->노->초 순으로 흐려지게 매핑
            # i가 커질수록(순위가 낮을수록) 리스트의 뒤쪽(흐린 초록) 색상이 선택됨
            idx = (i - 1) / (num_items - 2) if num_items > 2 else 0.5
            rgba = cmap(idx)
            hex_color = mcolors.to_hex(rgba)
            colors.append(hex_color)

    # 1등 무지개색 효과를 Plotly 바 내부 그라데이션(인라인 패턴)으로 직접 구현
    # Plotly에서는 특정 하나의 바에만 그라데이션을 주기 위해 color 주입 방식을 사용합니다.
    
    # --- 그래프 그리기 (Plotly) ---
    fig = go.Figure()

    # 1등 막대에 무지개 패턴 효과를 주기 위해 별도 분리하거나 컬러 배열 적용
    fig.add_trace(go.Bar(
        x=mbti_types,
        y=percentages,
        marker=dict(
            color=colors,
            line=dict(color='#333333', width=1)
        ),
        text=[f"{p:.2f}%" for p in percentages],
        textposition='auto',
    ))

    # 1등 막대 상단에 '🌈 1위' 표시 달아주기
    fig.add_annotation(
        x=mbti_types[0],
        y=percentages[0],
        text="🌈 1위",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-30,
        font=dict(size=14, color="black", family="Arial Black")
    )

    fig.update_layout(
        title=f"📊 {selected_country}의 MBTI 성격 유형 비율 (높은 순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%"),
        template="plotly_white",
        barrier=0.1
    )

    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 테이블 보여주기
    with st.expander("📄 원본 데이터 보기"):
        detail_df = pd.DataFrame({"MBTI": mbti_types, "비율 (%)": [f"{p:.2f}%" for p in percentages]})
        st.dataframe(detail_df, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 파일명을 확인하고 스크립트와 같은 폴더에 넣어주세요.")
