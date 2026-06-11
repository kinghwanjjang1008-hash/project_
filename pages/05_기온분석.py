import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 데이터 분석", layout="wide")
st.title("🌡️ 서울 기온 데이터 분석 웹 앱")

# 2. 데이터 로드 함수 (자동 인코딩 추적 및 캐싱 처리)
@st.cache_data
def load_data(path):
    # 한국어 데이터셋에서 자주 쓰이는 인코딩 목록
    encodings = ['cp949', 'euc-kr', 'utf-8', 'utf-8-sig']
    
    df = None
    for encode in encodings:
        try:
            df = pd.read_csv(path, encoding=encode)
            break  # 읽기 성공 시 루프 탈출
        except (UnicodeDecodeError, ValueError):
            continue
            
    if df is None:
        raise ValueError("파일의 인코딩을 찾을 수 없습니다. 파일 형식을 확인해주세요.")

    # 컬럼명 양끝 공백 제거 (기상청 데이터 특성)
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 변환 및 결측치 제거
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜'].str.strip(), errors='coerce')
        df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환 및 결측치 제거 예외 처리 수정
    dropna_cols = []
    if '최고기온' in df.columns:
        df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
        dropna_cols.append('최고기온')
    if '최저기온' in df.columns:
        df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
        dropna_cols.append('최저기온')
        
    # 존재하는 컬럼에 대해서만 결측치 제거
    if dropna_cols:
        df = df.dropna(subset=dropna_cols)
    
    return df

# 3. 파일 경로 설정 (지정된 경로 또는 현재 폴더 내 seoul.csv 검색)
possible_paths = ['seoul.csv', '../seoul.csv', 'pages/seoul.csv']
csv_path = None

for p in possible_paths:
    if os.path.exists(p):
        csv_path = p
        break

# 데이터 불러오기 실행
if csv_path:
    try:
        df = load_data(csv_path)
    except Exception as e:
        st.error(f"데이터를 처리하는 중 에러가 발생했습니다: {e}")
        st.stop()
else:
    st.error("📂 'seoul.csv' 파일을 찾을 수 없습니다. 파일이 깃허브 저장소에 업로드되었는지 확인해주세요.")
    st.stop()

# 4. 사이드바 - 날짜 선택 기능
st.sidebar.header("📅 조회 기간 설정")
min_date = df['날짜'].min().to_pydatetime()
max_date = df['날짜'].max().to_pydatetime()

# 사용자 날짜 범위 선택 (시작일, 종료일)
start_date, end_date = st.sidebar.date_input(
    "조회할 범위를 선택하세요",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 5. 데이터 필터링
filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]

# 6. 그래프 시각화 (바탕색: 흰색)
st.subheader(f"📈 {start_date} ~ {end_date} 기온 변화 그래프")

if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 배경색 흰색 설정
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # 꺾은선 그래프 그리기
    if '최고기온' in filtered_df.columns:
        ax.plot(filtered_df['날짜'], filtered_df['최고기온'], label='Max Temp', color='#ff4b4b', linewidth=2)
    if '최저기온' in filtered_df.columns:
        ax.plot(filtered_df['날짜'], filtered_df['최저기온'], label='Min Temp', color='#1f77b4', linewidth=2)
    
    # 스타일 지정 (스트림릿 클라우드 한글 깨짐 방지를 위해 영문 레이블 사용)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature (℃)', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # 스트림릿 화면에 출력
    st.pyplot(fig)
    
    # 하단 데이터 테이블 확장형태로 제공
    with st.expander("📊 선택한 기간 데이터 보기 (상세 테이블)"):
        show_cols = ['날짜']
        if '최저기온' in filtered_df.columns: show_cols.append('최저기온')
        if '최고기온' in filtered_df.columns: show_cols.append('최고기온')
        st.dataframe(filtered_df[show_cols].sort_values('날짜'), use_container_width=True)
else:
    st.warning("⚠️ 선택한 기간에 해당하는 데이터가 없습니다. (결측치 구간 여부 확인 요망)")
