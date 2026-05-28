import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 비율 시각화", layout="centered")

st.title("🌏 국가별 MBTI 비율 분석기")
st.markdown("국가를 선택하면 해당 국가의 MBTI 16가지 유형 비율을 확인하실 수 있습니다.")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    # CSV 파일을 읽어옵니다. (프로젝트 폴더 내 경로에 맞춰 파일이 있어야 합니다)
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

try:
    df = load_data()

    # 국가 선택 셀렉트박스
    country_list = sorted(df['Country'].unique())
    selected_country = st.selectbox("👉 국가를 선택하세요:", country_list)

    # 선택된 국가의 데이터 추출 및 정렬
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    # 비율이 높은 순서대로 정렬
    country_data = country_data.sort_values(ascending=False)

    mbti_types = country_data.index.tolist()
    percentages = (country_data.values * 100).tolist() # 백분율(%)로 변환

    # --- 색상 그라데이션 생성 ---
    colors = []
    num_items = len(mbti_types)
    
    # 2등부터 사용할 그라데이션 컬러맵 정의 (빨강 -> 주황 -> 노랑 -> 초록 순으로 연해짐)
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom_grad", ["#FF3333", "#FF9933", "#FFFF66", "#99FF99", "#E6FFE6"]
    )
    
    for i in range(num_items):
        if i == 0:
            # 1등 막대는 눈에 띄는 특별한 크림슨 레드(무지개 1위 어노테이션과 매칭)
            colors.append("crimson") 
        else:
            # 2등부터는 등수가 낮아질수록(i가 커질수록) 리스트 뒤쪽의 흐린 색상이 선택됨
            idx = (i - 1) / (num_items - 2) if num_items > 2 else 0.5
            rgba = cmap(idx)
            hex_color = mcolors.to_hex(rgba)
            colors.append(hex_color)

    # --- 그래프 그리기 (Plotly) ---
    fig = go.Figure()

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

    # 1등 막대 상단에 '🌈 1위' 풍선 도움말(Annotation) 달아주기
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

    # 레이아웃 설정 (에러 원인이었던 barrier 속성 제거 완료)
    fig.update_layout(
        title=f"📊 {selected_country}의 MBTI 성격 유형 비율 (높은 순)",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        yaxis=dict(ticksuffix="%"),
        template="plotly_white"
    )

    # 스트림릿 화면에 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 상세 데이터 테이블 보여주기
    with st.expander("📄 원본 데이터 보기"):
        detail_df = pd.DataFrame({
            "MBTI": mbti_types, 
            "비율 (%)": [f"{p:.2f}%" for p in percentages]
        })
        st.dataframe(detail_df, use_container_width=True)

except FileNotFoundError:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 메인 폴더(Root)에 파일이 올라가 있는지 확인해 주세요.")
