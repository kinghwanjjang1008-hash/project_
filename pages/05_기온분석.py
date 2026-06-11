import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 데이터 분석", layout="wide")
st.title("🌡️ 서울 기온 데이터 분석 웹 앱")

# 2. 데이터 로드 함수 (자동 인코딩 및 컬럼 자동 매핑)
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

    # 컬럼명 글자 양끝 공백 전처리
    df.columns = df.columns.str.strip()
    
    # [핵심 수정] 컬럼명 유연하게 찾기 (ex: '최고기온(℃)', '최고 기온' 모두 잡아냄)
    for col in df.columns:
        if '날짜' in col:
            df = df.rename(columns={col: '날짜'})
        elif '최고' in col:
            df = df.rename(columns={col: '최고기온'})
        elif '최저' in col:
            df = df.rename(columns={col: '최저기온'})

    # 날짜 처리
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜'].astype(str).str.strip(), errors='coerce')
        df = df.dropna(subset=['날짜'])
    
    # 기온 데이터 숫자형 변환 및 결측치 제거
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

# 데이터 불러오기 실행
if csv_path:
    try:
        df = load_data(csv_path)
    except Exception as e:
        st.error(f"데이터를 처리하는 중 에러가 발생했습니다: {e}")
        st.stop()
else:
    st.error("📂 'seoul.csv' 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
    st.stop()

# 4. 사이드바 - 날짜 선택 기능
st.sidebar.header("📅 조회 기간 설정")

min_date = df['날짜'].min().date()
max_date = df['날짜'].max().date()
# 기본 데이터는 너무 방대하지 않게 최근 1달 또는 1년 정도로 시작 유도
start_default = max(min_date, max_date - pd.Timedelta(days=365))

date_range = st.sidebar.date_input(
    "조회할 범위를 선택하세요",
    value=(start_default, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    
    # 5. 데이터 필터링 및 정렬
    filtered_df = df[(df['날짜'].dt.date >= start_date) & (df['날짜'].dt.date <= end_date)]
    filtered_df = filtered_df.sort_values('날짜')

    st.subheader(f"📈 {start_date} ~ {end_date} 기온 변화 그래프")

    if not filtered_df.empty:
        # 6. Plotly 차트 생성 (데이터를 완벽하게 강제 매핑)
        fig = go.Figure()
        
        # 최고기온 선 추가
        if '최고기온' in filtered_df.columns:
            fig.add_trace(go.Scatter(
                x=filtered_df['날짜'], 
                y=filtered_df['최고기온'], 
                mode='lines',
                name='최고기온(Max)',
                line=dict(color='#ff4b4b', width=2.5)  # 선을 조금 더 두껍게 설정
            ))
            
        # 최저기온 선 추가
        if '최저기온' in filtered_df.columns:
            fig.add_trace(go.Scatter(
                x=filtered_df['날짜'], 
                y=filtered_df['최저기온'], 
                mode='lines',
                name='최저기온(Min)',
                line=dict(color='#1f77b4', width=2.5)
            ))
            
        # 레이아웃 강제 지정 (바탕색 흰색 고정)
        fig.update_layout(
            plot_bgcolor='white',    
            paper_bgcolor='white',   
            font=dict(color='black'),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(220, 220, 220, 0.7)', 
                title="Date"
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(220, 220, 220, 0.7)', 
                title="Temperature (℃)"
            ),
            margin=dict(l=50, r=50, t=30, b=50),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 7. 하단 데이터 테이블
        with st.expander("📊 선택한 기간 데이터 보기 (상세 테이블)"):
            show_cols = ['날짜']
            if '최저기온' in filtered_df.columns: show_cols.append('최저기온')
            if '최고기온' in filtered_df.columns: show_cols.append('최고기온')
            st.dataframe(filtered_df[show_cols], use_container_width=True)
    else:
        st.warning("⚠️ 선택한 기간에 해당하는 데이터가 없습니다.")
else:
    st.info("💡 사이드바에서 시작일과 종료일을 모두 선택해 주세요.")
