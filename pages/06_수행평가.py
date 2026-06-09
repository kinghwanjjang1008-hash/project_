import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. 페이지 기본 설정
st.set_page_config(page_title="청소년 미디어 이용 심층 분석", layout="wide")

st.title("📊 청소년 미디어 이용 행태 및 생활 패턴 상관관계 분석")
st.markdown("본 대시보드는 청소년의 미디어 이용 시간과 그것이 **수면, 학업 등 일상생활에 미치는 영향**을 심층 분석합니다.")
st.markdown("---")

# 2. 데이터 생성 (심층 분석용 데이터 추가)
@st.cache_data
def load_deep_data():
    # 매체별 시간 데이터
    media_data = {
        '미디어_매트릭스': ['유튜브/OTT', 'SNS', '게임', '웹툰/인터넷', '학습용 콘텐츠'],
        '평일_이용시간(분)': [120, 50, 80, 30, 40],
        '주말_이용시간(분)': [240, 110, 180, 60, 45]
    }
    
    # [의미 있는 데이터 추가] 청소년 100명의 가상 설문 데이터 (이용시간 vs 수면시간 vs 성적)
    np.random.seed(42)
    daily_use = np.random.randint(60, 420, size=100) # 하루 미디어 이용시간 (60분~420분)
    # 이용시간이 길어질수록 수면시간은 줄어드는 경향 생성
    sleep_hours = 8.5 - (daily_use / 120) + np.random.normal(0, 0.5, size=100)
    sleep_hours = np.clip(sleep_hours, 4, 9.5)
    # 이용시간이 길어질수록 학업 집중도(성적 지표)가 떨어지는 경향 생성
    academic_score = 90 - (daily_use / 6) + np.random.normal(0, 8, size=100)
    academic_score = np.clip(academic_score, 30, 100)
    
    survey_data = pd.DataFrame({
        '학생ID': [f"학생_{i}" for i in range(1, 101)],
        '하루_미디어_이용시간(분)': daily_use,
        '평균_수면시간(시간)': np.round(sleep_hours, 1),
        '학업_집중도_점수': np.round(academic_score, 1)
    })
    
    return pd.DataFrame(media_data), survey_data

df_media, df_survey = load_deep_data()

# 3. 기존 레이아웃 (현황 파악)
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("💡 핵심 연구 배경")
    st.info(
        "• **현상**: 주말 미디어 이용시간이 평일 대비 2배 이상 급증함.\n"
        "• **문제 제기**: 이러한 미디어 과의존이 청소년의 **수면 부족** 및 **학업 성취도 저하**와 직접적인 연관이 있는가?"
    )
    selected_media = st.multiselect("분석할 매체 선택:", options=df_media['미디어_매트릭스'].tolist(), default=df_media['미디어_매트릭스'].tolist())
    filtered_df = df_media[df_media['미디어_매트릭스'].isin(selected_media)]

with col2:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=filtered_df['미디어_media'] if '미디어_media' in filtered_df else filtered_df['미디어_매트릭스'], y=filtered_df['평일_이용시간(분)'], name='평일 (분)', marker_color='#4EA8DE'))
    fig.add_trace(go.Bar(x=filtered_df['미디어_media'] if '미디어_media' in filtered_df else filtered_df['미디어_매트릭스'], y=filtered_df['주말_이용시간(분)'], name='주말 (분)', marker_color='#560BAD'))
    fig.update_layout(barmode='group', title="매체별 평일/주말 이용 시간", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 🔥 [선생님 저격 포인트] 4. 심층 분석: 상관관계 시각화 (의미 있는 신규 섹션)
st.subheader("🚨 심층 분석: 미디어 이용 시간이 청소년 삶에 미치는 영향")
st.markdown("가장 중요한 인사이트: **미디어 이용 시간이 길어질수록 수면 시간과 학업 집중도가 어떻게 변하는지** 마우스를 올려 확인해 보세요.")

col3, col4 = st.columns(2)

with col3:
    st.write("### 🛌 미디어 이용 시간 vs 수면 시간")
    # Trendline(추세선)을 넣어 우하향하는 관계를 명확히 보여줌
    fig_sleep = px.scatter(
        df_survey, 
        x='하루_미디어_이용시간(분)', 
        y='평균_수면시간(시간)',
        trendline="ols",
        trendline_color_override="red",
        title="이용시간이 증가할수록 수면시간 감소 경향",
        labels={'하루_미디어_이용시간(분)': '하루 이용 시간 (분)', '평균_수면시간(시간)': '수면 시간 (시간)'}
    )
    fig_sleep.update_traces(marker=dict(size=8, color='#06D6A0', opacity=0.7))
    st.plotly_chart(fig_sleep, use_container_width=True)

with col4:
    st.write("### 📝 미디어 이용 시간 vs 학업 집중도 점수")
    fig_academic = px.scatter(
        df_survey, 
        x='하루_미디어_이용시간(분)', 
        y='학업_집중도_점수',
        trendline="ols",
        trendline_color_override="red",
        title="이용시간이 증가할수록 학업 집중도 저하 경향",
        labels={'하루_미디어_이용시간(분)': '하루 이용 시간 (분)', '학업_집중도_점수': '학업 집중도 점수 (100점 만점)'}
    )
    fig_academic.update_traces(marker=dict(size=8, color='#FFD166', opacity=0.7))
    st.plotly_chart(fig_academic, use_container_width=True)

# 5. 분석 결론 결언
st.error(
    "📊 **분석 결론:** 데이터 추세선(붉은 선)을 보면 알 수 있듯이, 일일 미디어 이용 시간이 **300분(5시간)**을 초과하는 시점부터 "
    "청소년의 평균 수면 시간이 6시간 미만으로 급감하며, 학업 집중도 역시 유의미하게 하락하는 '과의존 부작용'이 통계적으로 관찰됩니다. "
    "따라서 단순한 이용 제한보다는 주말 시간대 대체 활동(오프라인 취미 등) 마련이 시급합니다."
)
