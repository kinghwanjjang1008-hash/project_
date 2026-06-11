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
        st.subheader("📌 국가별 MBTI 성향 확인")
        selected_country = st.selectbox("👉 분석할 국가를 선택하세요:", country_list, key="sb_country")

        country_rows = df[df['Country'] == selected_country]
        
        if not country_rows.empty:
            country_data = country_rows.iloc[0, 1:]
            country_data = country_data.sort_values(ascending=False)

            mbti_types_c = country_data.index.tolist()
            
            # 비율 데이터 안전 변환 (% 단위 고정)
            percentages_c = []
            for val in country_data.values:
                v = float(val)
                if v <= 1.0:
                    percentages_c.append(v * 100)
                else:
                    percentages_c.append(v)

            # 1등 Crimson 고정 및 2등 이하 그라데이션 색상 리스트 생성
            colors_tab1 = []
            num_items_c = len(mbti_types_c)
            cmap_c = mcolors.LinearSegmentedColormap.from_list("grad_c", ["#FF3333", "#FF9933", "#FFFF66", "#99FF99", "#E6FFE6"])
            
            for i in range(num_items_c):
                if i == 0:
                    colors_tab1.append("crimson") 
                else:
                    idx = (i - 1) / (num_items_c - 2) if num_items_c > 2 else 0.5
                    colors_tab1.append(mcolors.to_hex(cmap_c(idx)))

            # Plotly 막대그래프 시각화
            fig_c = go.Figure()
            
            text_labels_c = []
            for p in percentages_c:
                text_labels_c.append(f"{p:.2f}%")

            fig_c.add_trace(go.Bar(
                x=mbti_types_c, 
                y=percentages_c,
                marker=dict(color=colors_tab1, line=dict(color='#333333', width=1)),
                text=text_labels_c, 
                textposition='auto'
            ))
            
            # 1등 막대 위에 🌈 1위 표시
            fig_c.add_annotation(
                x=mbti_types_c[0], 
                y=percentages_c[0], 
                text="🌈 1위",
                showarrow=True, 
                arrowhead=2, 
                ax=0, 
                ay=-30, 
                font=dict(size=13, color="black", family="Arial Black")
            )
            
            fig_c.update_layout(
                title=f"📊 {selected_country}의 MBTI 유형별 비율 (높은 순)",
                xaxis_title="MBTI 성격 유형", 
                yaxis_title="비율 (%)",
                yaxis=dict(ticksuffix="%"), 
                template="plotly_white"
            )
            st.plotly_chart(fig_c, use_container_width=True)

            # 원본 데이터 보기
            with st.expander("📄 원본 데이터 펼쳐보기"):
                detail_df = pd.DataFrame({
                    "MBTI 유형": mbti_types_c, 
                    "비율 (%)": text_labels_c
                })
                st.dataframe(detail_df, use_container_width=True)
        else:
            st.warning("선택한 국가의 데이터가 존재하지 않습니다.")

    # ----------------------------------------------------------------
    # TAB 2: MBTI별 상위 국가 TOP 10 분석
    # ----------------------------------------------------------------
    with tab2:
        st.subheader("🏆 특정 MBTI가 가장 많은 나라 TOP 10")
        selected_mbti = st.selectbox("👉 MBTI 유형을 선택하세요:", all_mbti_types, key="sb_mbti")

        # 해당 MBTI를 기준으로 내림차순 정렬 후 상위 10개국 추출
        top10_df = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)
        
        countries_m = top10_df['Country'].tolist()
        
        # 비율 데이터 안전 변환 (% 단위 고정)
        percentages_m = []
        for val in top10_df[selected_mbti].values:
            v = float(val)
            if v <= 1.0:
                percentages_m.append(v * 100)
            else:
                percentages_m.append(v)

        # 10개 국가를 위한 독립된 색상 리스트 변수 정의
        colors_tab2 = []
        num_items_m = len(countries_m)
        cmap_m = mcolors.LinearSegmentedColormap.from_list("grad_m", ["#FF3333", "#FF9933", "#FFFF66", "#99FF99", "#E6FFE6"])
        
        for i in range(num_items_m):
            if i == 0:
                colors_tab2.append("crimson")
            else:
                idx = (i - 1) / (num_items_m - 2) if num_items_m > 2 else 0.5
                colors_tab2.append(mcolors.to_hex(cmap_m(idx)))

        # Plotly 막대그래프 시각화 (TOP 10)
        fig_m = go.Figure()
        
        text_labels_m = []
        for p in percentages_m:
            text_labels_m.append(f"{p:.2f}%")

        fig_m.add_trace(go.Bar(
            x=countries_m, 
            y=percentages_m,
            marker=dict(color=colors_tab2, line=dict(color='#333333', width=1)),
            text=text_labels_m, 
            textposition='auto'
        ))
        
        # 1등 국가 위에 🌈 1위 표시 생성
        if num_items_m > 0:
            fig_m.add_annotation(
                x=countries_m[0], 
                y=percentages_m[0], 
                text="🌈 1위",
                showarrow=True, 
                arrowhead=2, 
                ax=0, 
                ay=-30, 
                font=dict(size=13, color="black", family="Arial Black")
            )
            
        fig_m.update_layout(
            title=f"📊 전 세계 {selected_mbti} 비율 상위 10개국 순위",
            xaxis_title="국가명", 
            yaxis_title="비율 (%)",
            yaxis=dict(ticksuffix="%"), 
            template="plotly_white"
        )
        st.plotly_chart(fig_m, use_container_width=True)

        # 상세 데이터 테이블 구성
        with st.expander("📄 TOP 10 순위표 보기"):
            rank_list = []
            for i in range(num_items_m):
                rank_list.append(f"{i+1}위")

            detail_m_df = pd.DataFrame({
                "순위": rank_list,
                "국가명": countries_m,
                f"{selected_mbti} 비율 (%)": text_labels_m
            }).set_index("순위")
            st.dataframe(detail_m_df, use_container_width=True)
