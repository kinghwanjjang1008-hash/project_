import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 데이터 분석", layout="wide")
st.title("🌡️ 서울 기온 데이터 분석 웹 앱")

# 2. 데이터 로드 함수 (자동 인코딩 추적 및 캐싱 처리)
@st.cache_data
def load_data(path):
    encodings = ['cp949', 'euc-kr', 'utf-8', 'utf-8-sig']
    
    df = None
    for encode in encodings:
        try:
            df = pd.read_csv(path, encoding=encode)
            break
        except (UnicodeDecodeError, ValueError):
            continue
            
    if df is None:
        raise ValueError("파일의 인코딩을 찾을 수 없습니다. 파일 형식을 확인해주세요.")

    # 컬럼명 양끝 공백 제거 (기상청 데이터 고유 특성 해결)
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 변환 및 결측치 제거
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜'].str.strip(), errors='coerce')
        df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환 및 결측치 처리
    dropna_cols = []
    if '최고기온' in df.columns:
        df['최고기온'] = pd.to_numeric(df['최고기온'], errors='coerce')
        dropna_cols.append('최고기온')
    if '최저기온' in df.columns:
        df['최저기온'] = pd.to_numeric(df['최저기온'], errors='coerce')
        dropna_cols.append('최저기온')
        
    if dropna_cols:
        df = df.dropna(subset=dropna_cols)
    
    return df

# 3. 파일 경로 설정 (경로 유연성 확보)
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

# 4. 사이드바 - 날짜 선택 기능 (스트림릿 클라우드 전용 안전한 세팅)
st.sidebar.header("📅 조회 기간 설정")

# 판다스 Timestamp -> 순수 파이썬 date 객체로 안전하게 변환
min_date = df['날짜'].min().date()
max_date = df['날짜'].max().date()

# 기본 선택값은 마지막 날짜 기준 1년 전부터 마지막 날짜까지로 설정 (안전성 확보)
start_default = max(min_date, max_date - pd.Timedelta(days=365))

# 안전하게 세팅된 date 객체들을 입력
date_range = st.sidebar.date_input(
    "조회할 범위를 선택하세요",
    value=(start_default, max_date),
    min_value=min_date,
    max_value=max_date
)

# 사용자가 두 날짜(시작일, 종료일)를 모두 선택했을 때만 필터링 및 그래프 출력
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    
    # 5. 데이터 필터링
    filtered_df = df[(df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)]

    # 6. 그래프 시각화 (스트림릿 내장 고성능 차트 사용 -> 흰색 바탕 고정 및 마우스 오버 지원)
    st.subheader(f"📈 {start_date} ~ {end_date} 기온 변화 그래프")

    if not filtered_df.empty:
        # X축을 '날짜'로 잡기 위해 인덱스로 설정
        chart_data = filtered_df.set_index('날짜')
        
        # 표시할 컬럼 선택
        cols_to_show = []
        if '최고기온' in chart_data.columns: cols_to_show.append('최고기온')
        if '최저기온' in chart_data.columns: cols_to_show.append('최저기온')
        
        if cols_to_show:
            # 깔끔하게 흰색 바탕 테마를 따라가는 에러 없는 라인 차트
            st.line_chart(chart_data[cols_to_show], y_label="기온 (℃)")
        
        # 7. 하단 데이터 테이블 확장형태 제공
        with st.expander("📊 선택한 기간 데이터 보기 (상세 테이블)"):
            show_cols = ['날짜'] + cols_to_show
            st.dataframe(filtered_df[show_cols].sort_values('날짜'), use_container_width=True)
    else:
        st.warning("⚠️ 선택한 기간에 해당하는 데이터가 없습니다.")
else:
    st.info("💡 사이드바에서 달력 창을 열어 시작일과 종료일을 모두 선택해 주세요.")
