import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.colors as mcolors

# 스트림릿 웹페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 데이터 분석기", layout="centered")

st.title("🌏 전 세계 MBTI 데이터 분석기")
st.markdown("원하는 분석 탭을 선택하여 국가별 또는 MBTI 유형별 데이터를 확인해 보세요.")

# 데이터 캐싱 처리
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except Exception:
        return None

df = load_data()

# 데이터 로드 실패 시 예외 처리
if df is None:
    st.error("❌ `countriesMBTI_16types.csv` 파일을 찾을 수 없습니다. 파일이 프로젝트 최상위 폴더(Root)에 업로드되어 있는지 확인해 주세요.")
else:
    all_mbti_types = df.columns[1:].tolist()
    country_list = sorted(df['Country'].dropna().unique())

    # 탭 구성
    tab1, tab2 = st.tabs(["📍 국가별 MBTI 비율", "📊 MBTI별 상위 국가 TOP 10"])

    # ----------------------------------------------------------------
    # TAB 1: 국가별 MBTI 비율 분석
    # ----------------------------------------------------------------
    with tab1:
        st.subheader("
