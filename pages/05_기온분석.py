import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정 (깨짐 방지)
plt.rcParams['font.family'] = 'Malgun Gothic' # 윈도우 기준 (맥은 'AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

st.title("🌡️ 기온 데이터 분석")

# 1. 데이터 로드 함수 수정
@st.cache_data
def load_sample_data():
    # 예시 데이터를 위한 날짜 생성
    dates = pd.date_range(start="2026-06-01", periods=10)
    
    # 임의의 기온 데이터 생성 (시리즈 형태)
    min_temps = pd.Series([15.45, 16.12, 14.89, 15.01, 16.78, 17.23, 15.60, 14.95, 16.34, 15.88])
    max_temps = pd.Series([25.34, 27.89, 24.56, 26.11, 28.45, 29.12, 26.78, 25.45, 27.23, 26.90])
    
    # 💡 해결 포인트: round() 대신 판다스의 .round(1)을 사용합니다.
    df = pd.DataFrame({
        '날짜': dates,
        '최저기온': min_temps.round(1),
        '최고기온': max_temps.round(1)
    })
    
    return df

# 데이터 불러오기
df = load_sample_data()

# 2. 데이터 프리뷰 데이터프레임 출력
st.subheader("기온 데이터 표")
st.dataframe(df)

---

# 3. 그래프 그리기 및 범례 표시
st.subheader("기온 변화 그래프")

fig, ax = plt.subplots(figsize=(10, 5))

# 최고기온, 최저기온 선 그래프 그리기 (label 속성이 범례 이름이 됩니다)
ax.plot(df['날짜'], df['최고기온'], marker='o', color='red', label='최고기온 (Max)')
ax.plot(df['날짜'], df['최저기온'], marker='o', color='blue', label='최저기온 (Min)')

# 그래프 꾸미기
ax.set_title("날짜별 기온 변화 동향", fontsize=16)
ax.set_xlabel("날짜", fontsize=12)
ax.set_ylabel("기온 (°C)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)

# 💡 범례(Legend) 표시 활성화
ax.legend(loc='upper right', fontsize=11, shadow=True)

# 스트림릿에 matplotlib 그래프 출력
st.pyplot(fig)
