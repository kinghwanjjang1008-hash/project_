import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 한글 폰트 설정 (Streamlit Cloud 환경 고려)
plt.rcParams['font.family'] = 'NanumGothic' or 'Malgun Gothic' or 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("📅 서울 일별 기온 변화 조회")
st.write("원하는 월과 일을 선택하면 역대 해당 날짜의 최고/최저 기온 추이를 보여줍니다.")

# 1. 데이터 로드 (상위 폴더의 seoul.csv 읽기)
csv_path = os.path.join("..", "seoul.csv")

@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        # 로컬 환경이나 경로 에러 방지를 위해 현재 디렉토리도 확인
        if os.path.exists("seoul.csv"):
            path = "seoul.csv"
        else:
            st.error("❌ seoul.csv 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
            return None
            
    df = pd.read_csv(path, encoding='utf-8')
    
    # 날짜 데이터 앞뒤 공백 및 탭 문자 제거
    df['날짜'] = df['날짜'].astype(str).str.strip()
    
    # datetime 형태로 변환 (변환 실패 시 NaT 처리)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    df = df.dropna(subset=['날짜'])
    
    # 월, 일 컬럼 생성
    df['Month'] = df['날짜'].dt.month
    df['Day'] = df['날짜'].dt.day
    df['Year'] = df['날짜'].dt.year
    
    return df

df = load_data(csv_path)

if df is not None:
    # 2. 사이드바에서 월/일 선택 UI 구성
    st.sidebar.header("🗓️ 날짜 선택")
    selected_month = st.sidebar.selectbox("월(Month)을 선택하세요", list(range(1, 13)), index=5) # 기본값 6월
    
    # 선택한 월에 맞는 일 수 계산 (단순화하여 1~31일 제공 후 데이터 필터링)
    selected_day = st.sidebar.selectbox("일(Day)을 선택하세요", list(range(1, 32)), index=3) # 기본값 4일
    
    # 3. 데이터 필터링
    filtered_df = df[(df['Month'] == selected_month) & (df['Day'] == selected_day)].sort_values('Year')
    
    if filtered_df.empty:
        st.warning(f"⚠️ {selected_month}월 {selected_day}일에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📈 역대 {selected_month}월 {selected_day}일 기온 변화")
        
        # 4. 꺾은선 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # 최고기온: 빨강(red), 최저기온: 연한 파랑(lightblue)
        ax.plot(filtered_df['Year'], filtered_df['최고기온(℃)'], marker='o', color='red', label='최고기온(℃)', linewidth=2)
        ax.plot(filtered_df['Year'], filtered_df['최저기온(℃)'], marker='o', color='lightblue', label='최저기온(℃)', linewidth=2)
        
        ax.set_title(f"Every {selected_month}/{selected_day} Temperature Trend", fontsize=14)
        ax.set_xlabel("연도 (Year)", fontsize=11)
        ax.set_ylabel("기온 (Temperature ℃)", fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        
        # 스트림릿에 그래프 출력
        st.pyplot(fig)
        
        # 5. 데이터 테이블 보여주기 (선택사항)
        with st.expander("📊 상세 데이터 보기"):
            view_df = filtered_df[['Year', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True)
            st.dataframe(view_df)
