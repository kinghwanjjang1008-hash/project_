import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 데이터 분석", layout="wide")
st.title("🌡️ 서울 기온 데이터 분석 웹 앱")

# 2. 데이터 로드 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 파일명은 seoul.csv로 가정합니다.
    try:
        df = pd.read_csv('seoul.csv', encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv('seoul.csv', encoding='utf-8')
    
    # 컬럼명 양끝 공백 제거 (기상청 데이터 특성 반영)
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 변환 및 결측치 제거
    df['날짜'] = pd.to_datetime(df['날짜'].str.strip(), errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환 및 결측치 제거
    df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
    df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
    df = df.dropna(subset=['최고기온', '최저기온'])
    
    return df

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 읽는 중 오류가 발생했습니다. 'seoul.csv' 파일이 같은 폴더에 있는지 확인해주세요. 에러 내용: {e}")
    st.stop()

# 3. 사이드바 - 날짜 선택 기능
st.sidebar.header("📅 조회 기간 설정")
min_date = df['날짜'].min().to_pydatetime()
max_date = df['날짜'].max().to_pydatetime()

# 사용자로부터 시작일과 종료일 입력 받기
start_date, end_date = st.sidebar.date_input(
    "조회할 범위를 선택하세요",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 4. 데이터 필터링
filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]

# 5. 그래프 시각화 (바탕색: 흰색)
st.subheader(f"📈 {start_date} ~ {end_date} 기온 변화 그래프")

if not filtered_df.empty:
    # 한글 깨짐 방지 설정
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우용 기본 폰트
    plt.rcParams['axes.unicode_minus'] = False     # 마이너스 기호 깨짐 방지

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 배경색 흰색 설정 (요청 반영)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # 꺾은선 그래프 그리기
    ax.plot(filtered_df['날짜'], filtered_df['최고기온'], label='최고기온', color='#ff4b4b', linewidth=2)
    ax.plot(filtered_df['날짜'], filtered_df['최저기온'], label='최저기온', color='#1f77b4', linewidth=2)
    
    # 레이블 및 스타일 지정
    ax.set_xlabel('날짜', fontsize=12)
    ax.set_ylabel('기온 (℃)', fontsize=12)
    ax.title.set_text('최고/최저 기온 추이')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 스트림릿에 그래프 출력
    st.pyplot(fig)
    
    # 데이터 테이블도 살짝 보여주기
    with st.expander("📊 선택한 기간 데이터 보기"):
        st.dataframe(filtered_df[['날짜', '최저기온', '최고기온']].sort_values('날짜'))
else:
    st.warning("선택한 기간에 해당하는 데이터가 없습니다. (6.25 전쟁 기간 등 결측치 확인 요망)")
