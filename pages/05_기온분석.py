import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="날씨 데이터 시각화", layout="centered")
st.title("🌡️ 날짜별 최고/최저 기온 조회")

# 2. 샘플 데이터 생성 (2026년 1월 ~ 12월)
# 실제 데이터 파일(CSV 등)이 있다면 이 부분을 데이터프레임 로드 코드로 바꾸시면 됩니다.
@st.cache_data
def load_sample_data():
    date_range = pd.date_range(start="2026-01-01", end="2026-12-31")
    # 예시를 위한 가상 기온 데이터 생성
    import numpy as np
    np.random.seed(42)
    base_temp = 15 + 15 * np.sin(2 * np.pi * (date_range.dayofyear - 150) / 365)
    min_temps = base_temp - np.random.uniform(5, 10, size=len(date_range))
    max_temps = base_temp + np.random.uniform(5, 10, size=len(date_range))
    
    df = pd.DataFrame({
        '날짜': date_range.date,
        '최저기온': round(min_temps, 1),
        '최고기온': round(max_temps, 1)
    })
    return df

df = load_sample_data()

# 3. 사이드바에서 날짜 범위 선택 (기본값: 최근 일주일)
st.sidebar.header("📅 기간 선택")
today = datetime.date(2026, 6, 4) # 기준일
start_date = st.sidebar.date_input("시작일", today - datetime.timedelta(days=7))
end_date = st.sidebar.date_input("종료일", today)

# 날짜 유효성 검사
if start_date > end_date:
    st.error("시작일은 종료일보다 이전이어야 합니다.")
else:
    # 4. 선택한 날짜로 데이터 필터링
    filtered_df = df[(df['날짜'] >= start_date) & (df['날짜'] <= end_date)]
    filtered_df = filtered_df.sort_values(by='날짜')

    if filtered_df.empty:
        st.warning("선택한 기간에 해당하는 데이터가 없습니다.")
    else:
        # 5. Plotly를 이용한 꺾은선 그래프 그리기
        fig = go.Figure()

        # 최고기온 선 (빨간색)
        fig.add_trace(go.Scatter(
            x=filtered_df['날짜'], 
            y=filtered_df['최고기온'],
            mode='lines+markers',
            name='최고기온',
            line=dict(color='red', width=3),
            marker=dict(size=6)
        ))

        # 최저기온 선 (연한 파란색 - Light Sky Blue)
        fig.add_trace(go.Scatter(
            x=filtered_df['날짜'], 
            y=filtered_df['최저기온'],
            mode='lines+markers',
            name='최저기온',
            line=dict(color='lightskyblue', width=3),
            marker=dict(size=6)
        ))

        # 그래프 레이아웃 설정 (흰색 바탕 및 한글 설정)
        fig.update_layout(
            title=f"<b>{start_date} ~ {end_date} 기온 변화</b>",
            xaxis_title="날짜",
            yaxis_title="기온 (°C)",
            template="plotly_white",  # 흰색 배경 바탕
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # 스트림릿에 그래프 출력
        st.plotly_chart(fig, use_container_width=True)

        # 6. 데이터 표 출력
        st.subheader("📋 선택한 기간의 데이터 상세")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
