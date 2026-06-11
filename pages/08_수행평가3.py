import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 기본 설정
st.set_page_config(page_title="공항별 출입국 심층 분석 대시보드", layout="wide")

# 2. 자유롭게 움직이는 승무원 스티커 HTML/CSS/JS 주입
st.markdown("""
    <div id="crew-sticker" style="
        position: fixed;
        bottom: 50px;
        right: 50px;
        font-size: 50px;
        cursor: move;
        z-index: 9999;
        user-select: none;
        background: rgba(255,255,255,0.8);
        padding: 10px;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    ">🧑‍✈️</div>

    <script>
        const sticker = document.getElementById('crew-sticker');
        let isDragging = false;
        let offsetX, offsetY;

        sticker.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - sticker.getBoundingClientRect().left;
            offsetY = e.clientY - sticker.getBoundingClientRect().top;
            sticker.style.position = 'fixed';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            sticker.style.left = (e.clientX - offsetX) + 'px';
            sticker.style.top = (e.clientY - offsetY) + 'px';
            sticker.style.bottom = 'auto';
            sticker.style.right = 'auto';
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        sticker.addEventListener('touchstart', (e) => {
            isDragging = true;
            const touch = e.touches[0];
            offsetX = touch.clientX - sticker.getBoundingClientRect().left;
            offsetY = touch.clientY - sticker.getBoundingClientRect().top;
        });

        document.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            const touch = e.touches[0];
            sticker.style.left = (touch.clientX - offsetX) + 'px';
            sticker.style.top = (touch.clientY - offsetY) + 'px';
            sticker.style.bottom = 'auto';
            sticker.style.right = 'auto';
        });

        document.addEventListener('touchend', () => {
            isDragging = false;
        });
    </script>
""", unsafe_allow_html=True)

# 3. 데이터 로드 및 파생변수 생성 (TypeError 및 인코딩 오류 완벽 해결)
@st.cache_data
def load_data():
    file_path = "법무부_항공기 및 승무원에 대한 국적별 공항별 출입국 현황_20241231 (1).csv"
    
    # cp949 인코딩을 적용하고, 판다스 버전에 맞는 encoding_errors 인자를 사용하여 TypeError를 방지합니다.
    df = pd.read_csv(file_path, encoding='cp949', encoding_errors='ignore')
    
    # 공항별 텍스트 공백 제거 (예: '사 천 항' -> '사천항')
    df['공항별'] = df['공항별'].str.replace(' ', '')
    
    # [의미 추가 1] 항공기 1대당 승무원 배정 비율 (밀도) 계산
    df['입항_항공기당승무원수'] = df.apply(lambda r: round(r['입항승무원수'] / r['입항항공기수'], 1) if r['입항항공기수'] > 0 else 0, axis=1)
    df['출항_항공기당승무원수'] = df.apply(lambda r: round(r['출항승무원수'] / r['출항항공기수'], 1) if r['출항항공기수'] > 0 else 0, axis=1)
    
    # [의미 추가 2] 출입국 수지 불균형 지표 (출항 - 입항)
    df['항공기_출입차이'] = df['출항항공기수'] - df['입항항공기수']
    df['승무원_출입차이'] = df['출항승무원수'] - df['입항승무원수']
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("CSV 파일을 찾을 수 없습니다. 깃허브 저장소에 '법무부_항공기 및 승무원에 대한 국적별 공항별 출입국 현황_20241231 (1).csv' 파일이 대시보드 파일과 같은 위치에 있는지 확인해 주세요.")
    st.stop()

# 4. 타이틀 및 대시보드 소개
st.title("🛬 공항별 출입국 현황 및 트렌드 인사이트 대시보드")
st.caption("단순 수치 조회를 넘어, 운항 효율성과 출입국 흐름의 의미를 분석하는 딥 애널리시스 뷰입니다.")

st.markdown("---")

# 5. 상단 핵심 요약 지표 (Metric)
total_in_planes = df["입항항공기수"].sum()
total_out_planes = df["출항항공기수"].sum()
avg_crew_per_plane = round(df["입항승무원수"].sum() / df["입항항공기수"].sum(), 1)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 입항 항공기", f"{total_in_planes:,} 대")
with col2:
    st.metric("총 출항 항공기", f"{total_out_planes:,} 대")
with col3:
    st.metric("전체 평균 항공기당 승무원 수", f"{avg_crew_per_plane} 명", help="전체 입항 승무원을 전체 입항 항공기 수로 나눈 대한민국 평균값입니다.")

st.markdown("---")

# 6. 분석 탭 구조
tab1, tab2, tab3 = st.tabs(["📊 기본 현황 조회", "💡 [인사이트] 항공기당 승무원 밀도", "⚖️ [인사이트] 출입국 흐름 불균형"])

# --- TAB 1: 기본 현황 조회 (브라운 테마) ---
with tab1:
    st.subheader("공항별 기본 규모 비교")
    data_type = st.radio("시각화할 기본 데이터 선택", ["항공기 수", "승무원 수"], horizontal=True, key="base_data")
    
    if data_type == "항공기 수":
        fig1 = px.bar(
            df, x="공항별", y=["입항항공기수", "출항항공기수"], barmode="group",
            title="공항별 항공기 통계", color_discrete_sequence=['#4A3525', '#8B5A2B']
        )
    else:
        fig1 = px.bar(
            df, x="공항별", y=["입항승무원수", "출항승무원수"], barmode="group",
            title="공항별 승무원 통계", color_discrete_sequence=['#8B4513', '#CD853F']
        )
        
    fig1.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', hovermode="x unified", 
        font=dict(color='#4A3525'), title_font=dict(size=16, color='#4A3525')
    )
    fig1.update_xaxes(showgrid=True, gridcolor='#E6D7C3')
    fig1.update_yaxes(showgrid=True, gridcolor='#E6D7C3')
    st.plotly_chart(fig1, use_container_width=True)


# --- TAB 2: 항공기당 승무원 밀도 분석 (대형기 취항 여부 의미 분석) ---
with tab2:
    st.subheader("✈️ 공항별 항공기 1대당 평균 승무원 수 분석")
    st.markdown("""
        **💡 분석의 의미:** 항공기 1대당 탑승한 승무원 수가 많을수록 해당 공항에는 주로 **대형 항공기(광동체기)**가 취항하거나 장거리 노선 위주로 편성되어 있음을 시사합니다. 반대로 수치가 낮다면 소형기나 단거리 노선 중심의 공항입니다.
    """)
    
    fig2 = px.bar(
        df, x="공항별", y=["입항_항공기당승무원수", "출항_항공기당승무원수"], barmode="group",
        title="공항별 항공기 1대당 탑승 승무원 비율 (운항 규모 지표)",
        color_discrete_sequence=['#A0522D', '#DEB887'],
        labels={"value": "평균 승무원 수 (명)", "variable": "구분"}
    )
    
    fig2.add_hline(y=avg_crew_per_plane, line_dash="dash", line_color="#4A3525", 
                  annotation_text=f"전국 평균 ({avg_crew_per_plane}명)", annotation_position="top left")
    
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', hovermode="x unified", 
        font=dict(color='#4A3525'), title_font=dict(size=16, color='#4A3525')
    )
    fig2.update_xaxes(showgrid=True, gridcolor='#E6D7C3')
    fig2.update_yaxes(showgrid=True, gridcolor='#E6D7C3')
    st.plotly_chart(fig2, use_container_width=True)


# --- TAB 3: 출입국 흐름 불균형 분석 (수지 분석) ---
with tab3:
    st.subheader("⚖️ 입항과 출항의 차이 분석 (수지 및 흐름 불균형)")
    st.markdown("""
        **💡 분석의 의미:** * **(+) 양수 값 (위로 솟은 바):** 들어온 것보다 **나간 것(출항)이 많음**
        * **(-) 음수 값 (아래로 꺼진 바):** 들어온 것보다 **덜 나감**
    """)
    
    diff_type = st.selectbox("분석할 대상을 선택하세요", ["승무원 출입 차이 (출항-입항)", "항공기 출입 차이 (출항-입항)"])
    
    if "승무원" in diff_type:
        target_col = "승무원_출입차이"
        title_text = "공항별 승무원 출입 불균형 (출항수 - 입항수)"
        bar_color = '#6E473B'
    else:
        target_col = "항공기_출입차이"
        title_text = "공항별 항공기 출입 불균형 (출항수 - 입항수)"
        bar_color = '#8C6239'
        
    fig3 = px.bar(
        df, x="공항별", y=target_col,
        title=title_text,
        color_discrete_sequence=[bar_color]
    )
    
    fig3.add_hline(y=0, line_color="black", line_width=1.5)
    fig3.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', 
        font=dict(color='#4A3525'), title_font=dict(size=16, color='#4A3525')
    )
    fig3.update_xaxes(showgrid=True, gridcolor='#E6D7C3')
    fig3.update_yaxes(showgrid=True, gridcolor='#E6D7C3')
    st.plotly_chart(fig3, use_container_width=True)

# 7. 원본 데이터 토글 확인 세션
st.markdown("---")
with st.expander("📄 데이터셋 원본 및 자동 계산된 인덱스 데이터 확인"):
    st.dataframe(df, use_container_width=True)
