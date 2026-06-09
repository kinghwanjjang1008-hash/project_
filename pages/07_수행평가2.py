import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# --- 페이지 설정 ---
st.set_page_config(page_title="2025 항공 여객 통계 대시보드", layout="wide")

# --- 비행기 애니메이션 및 스타일 CSS ---
st.markdown("""
    <style>
    /* 비행기가 화면을 가로지르는 애니메이션 */
    @keyframes fly {
        0% { left: -10%; top: 10%; transform: rotate(10deg); }
        50% { top: 15%; }
        100% { left: 110%; top: 5%; transform: rotate(10deg); }
    }
    .airplane {
        position: fixed;
        font-size: 50px;
        z-index: 9999;
        pointer-events: none;
        animation: fly 15s linear infinite;
    }
    .main {
        background-color: #f0f2f6;
    }
    </style>
    <div class="airplane">✈️</div>
    """, unsafe_allow_html=True)

# --- 데이터 로드 ---
data = """연도,항공사,노선,정기부정기,여객도착,여객출발
2025,아시아나항공,국내,정기,2953007,2953007
2025,아시아나항공,국내,부정기,39906,39906
2025,아시아나항공,국제,정기,4089187,4090664
2025,아시아나항공,국제,부정기,64934,61758
2025,대한항공,국내,정기,4176446,4176446
2025,대한항공,국내,부정기,69955,69955
2025,대한항공,국제,정기,6339485,6325980
2025,대한항공,국제,부정기,35198,35619
2025,에어부산,국내,정기,1591724,1591724
2025,에어부산,국내,부정기,1322,1322
2025,에어부산,국제,정기,1354933,1350015
2025,에어부산,국제,부정기,30906,29913
2025,이스타항공,국내,정기,1751173,1751173
2025,이스타항공,국내,부정기,24747,24747
2025,이스타항공,국제,정기,906592,901881
2025,이스타항공,국제,부정기,10645,9762
2025,제주항공,국내,정기,2852159,2852159
2025,제주항공,국내,부정기,43389,43389
2025,제주항공,국제,정기,2529908,2497360
2025,제주항공,국제,부정기,23357,22420
2025,진에어,국내,정기,2861455,2861455
2025,진에어,국내,부정기,9784,9784
2025,진에어,국제,정기,2305228,2285576
2025,진에어,국제,부정기,42291,44076
2025,티웨이항공,국내,정기,2564824,2564824
2025,티웨이항공,국내,부정기,122292,122292
2025,티웨이항공,국제,정기,2274552,2264924
2025,티웨이항공,국제,부정기,20210,19916
2025,에어프레미아,국제,정기,317753,341679
2025,에어프레미아,국제,부정기,6090,5068
2025,에어서울,국내,정기,360138,360138
2025,에어서울,국제,정기,579026,582496
2025,비엣젯항공,국제,정기,1028944,935806
2025,중국동방항공,국제,정기,864267,864339
2025,싱가포르항공,국제,정기,265509,274977
"""
# 데이터가 너무 많아 샘플링해서 넣었습니다. 실제 파일이 있다면 pd.read_csv("파일명.csv")를 사용하세요.

df = pd.read_csv(StringIO(data))
df['총여객'] = df['여객도착'] + df['여객출발']

# --- 메인 타이틀 ---
st.title("✈️ 2025 항공사 여객 실적 분석")
st.markdown("항공사별 노선 실적 및 출발/도착 여객 수를 실시간으로 확인하세요.")

# --- 사이드바 필터 ---
st.sidebar.header("📍 데이터 필터링")
selected_route = st.sidebar.multiselect("노선 선택", options=df['노선'].unique(), default=df['노선'].unique())
selected_airline = st.sidebar.multiselect("항공사 선택", options=df['항공사'].unique(), default=df['항공사'].unique()[:5])

filtered_df = df[(df['노선'].isin(selected_route)) & (df['항공사'].isin(selected_airline))]

# --- 주요 지표 (KPI) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 여객 수", f"{filtered_df['총여객'].sum():,}")
with col2:
    st.metric("총 출발 여객", f"{filtered_df['여객출발'].sum():,}")
with col3:
    st.metric("총 도착 여객", f"{filtered_df['여객도착'].sum():,}")

st.markdown("---")

# --- 시각화 1: 항공사별 출발/도착 비교 (Grouped Bar) ---
st.subheader("🛫 항공사별 출발 vs 도착 여객 분석")
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=filtered_df['항공사'], y=filtered_df['여객출발'], name='출발 여객', marker_color='#1f77b4'))
fig1.add_trace(go.Bar(x=filtered_df['항공사'], y=filtered_df['여객도착'], name='도착 여객', marker_color='#ff7f0e'))

fig1.update_layout(
    barmode='group',
    xaxis_title="항공사",
    yaxis_title="여객 수",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig1, use_container_width=True)

# --- 시각화 2: 국내 vs 국제 노선 비중 (Pie Chart) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🗺️ 노선별 여객 비중")
    fig2 = px.pie(filtered_df, values='총여객', names='노선', hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.subheader("📊 정기 vs 부정기 항공편 분석")
    fig3 = px.sunburst(filtered_df, path=['노선', '정기부정기'], values='총여객',
                      color='노선', color_discrete_map={'국내':'#636EFA', '국제':'#EF553B'})
    st.plotly_chart(fig3, use_container_width=True)

# --- 시각화 3: 항공사 실적 순위 (Treemap) ---
st.subheader("🏆 항공사별 점유율 (Treemap)")
st.info("비행기 아이콘을 클릭하듯 박스를 클릭하면 상세 내역을 볼 수 있습니다.")
fig4 = px.treemap(filtered_df, path=['항공사', '노선'], values='총여객',
                 color='총여객', color_continuous_scale='Blues')
st.plotly_chart(fig4, use_container_width=True)

# --- 하단 데이터 테이블 ---
if st.checkbox("상세 데이터 보기"):
    st.dataframe(filtered_df.style.format({'여객도착': '{:,}', '여객출발': '{:,}', '총여객': '{:,}'}))
