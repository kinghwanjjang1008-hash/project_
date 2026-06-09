import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(page_title="청소년 미디어 이용 행태 분석", layout="wide")

st.title("📊 청소년 미디어 이용 시간 및 행태 분석 대시보드")
st.markdown("본 대시보드는 청소년의 평일/주말 미디어 이용 시간과 스마트폰 과의존 현황을 분석합니다.")
st.markdown("---")

# 2. 샘플 데이터 생성 (실제 CSV 파일이 있다면 pd.read_csv 사용)
# 수행평가 시연 및 작동을 위해 완벽한 형태의 가상 데이터를 기본 탑재해 둡니다.
@st.cache_data
def load_data():
    # 실제 데이터 가공 형태와 유사하게 구성
    data = {
        '미디어_매트릭스': ['유튜브/OTT', 'SNS', '게임', '웹툰/인터넷', '학습용 콘텐츠'],
        '평일_이용시간(분)': [120, 50, 80, 30, 40],
        '주말_이용시간(분)': [240, 110, 180, 60, 45]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. 레이아웃 분할 (위젯 및 주요 지표)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("💡 주요 분석 포인트")
    st.info(
        "• **주말 미디어 폭증**: 평일 대비 주말에 유튜브 및 게임 이용 시간이 2배 이상 급증합니다.\n"
        "• **과몰입 위험군 관리**: 스마트폰 고위험군 청소년의 경우 주말 이용 시간이 평균 5시간을 초과하는 경향을 보입니다."
    )
    
    # 인터랙티브 사이드바 또는 선택 위젯
    selected_media = st.multiselect(
        "분석할 미디어 매체를 선택하세요:",
        options=df['미디어_매트릭스'].tolist(),
        default=df['미디어_매트릭스'].tolist()
    )
    
    filtered_df = df[df['미디어_매트릭스'].isin(selected_media)]

with col2:
    st.subheader("⏱️ 매체별 평일 vs 주말 이용 시간 비교")
    
    # Plotly를 활용한 그룹 바 차트 시각화
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=filtered_df['미디어_매트릭스'],
        y=filtered_df['평일_이용시간(분)'],
        name='평일 (분)',
        marker_color='#4EA8DE'
    ))
    fig.add_trace(go.Bar(
        x=filtered_df['미디어_매트릭스'],
        y=filtered_df['주말_이용시간(분)'],
        name='주말 (분)',
        marker_color='#560BAD'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="미디어 매체",
        yaxis_title="이용 시간 (분)",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. 하단 추가 분석 (스마트폰 과의존 위험군 비율 - 파이차트)
st.subheader("🚨 청소년 스마트폰 과의존 위험군 현황")

col3, col4 = st.columns([2, 1])

with col3:
    # 파이 차트 데이터
    risk_data = {
        '상태': ['일반 사용자군', '잠재적 위험군', '고위험군'],
        '비율(%)': [72.5, 22.1, 5.4]
    }
    df_risk = pd.DataFrame(risk_data)
    
    fig_pie = px.pie(
        df_risk, 
        values='비율(%)', 
        names='상태', 
        color_discrete_sequence=['#2EC4B6', '#FF9F1C', '#E71D36'],
        hole=0.4
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.write("")
    st.write("")
    st.metric(label="⚠️ 고위험군 비율", value="5.4 %", delta="전년 대비 0.8% 증가", delta_color="inverse")
    st.metric(label="🛡️ 잠재적 위험군 비율", value="22.1 %", delta="전년 대비 1.2% 증가", delta_color="inverse")
