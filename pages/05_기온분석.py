import streamlit as st
import pandas as pd
import os

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

    # 컬럼명 양끝 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 데이터 변환 및 결측치 제거
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜'].str.strip(), errors='coerce')
        df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환
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

# 3. 파일 경로 설정
possible_paths = ['seoul.csv', '../seoul.csv', 'pages/seoul.csv']
csv_path = None

for p in possible_paths:
    if os.path.exists(p):
        csv_path = p
        break

# 데이터 불러오기
if csv_path:
    try:
        df = load_data(csv_path)
    except Exception as e:
        st.error(f"데이터를 처리하는 중 에러가 발생했습니다: {e}")
        st.stop()
else:
    st.error("📂 'seoul.csv' 파일을 찾을 수 없습니다.")
    st.stop()

# 4. 사이드바 - 날짜 선택 기능
st.sidebar.header("📅 조회 기간 설정")
min_date = df['날짜'].min().to_pydatetime()
max_date = df['날짜'].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    "조회할 범위를 선택하세요",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 5. 데이터 필터링
filtered_df = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]

# 6. 그래프 시각화 (스트림릿 내장 고성능 차트 사용)
st.subheader(f"📈 {start_date} ~ {end_date} 기온 변화 그래프")

if not filtered_df.empty:
    # 차트에 그릴 데이터 재정렬 (X축을 '날짜'로 잡기 위함)
    chart_data = filtered_df.set_index('날짜')
    
    # 표시할 컬럼 선택
    cols_to_show = []
    if '최고기온' in chart_data.columns: cols_to_show.append('최고기온')
    if '최저기온' in chart_data.columns: cols_to_show.append('최저기온')
    
    if cols_to_show:
        # 스트림릿 내장 라인 차트 (에러가 없고, 마우스를 올리면 숫자가 보임)
        # 흰색 바탕 테마를 확실히 타도록 디자인됩니다.
        st.line_chart(chart_data[cols_to_show], y_label="기온 (℃)")
    
    # 하단 데이터 테이블
    with st.expander("📊 선택한 기간 데이터 보기 (상세 테이블)"):
        show_cols = ['날짜'] + cols_to_show
        st.dataframe(filtered_df[show_cols].sort_values('날짜'), use_container_width=True)
else:
    st.warning("⚠️ 선택한 기간에 해당하는 데이터가 없습니다.")
