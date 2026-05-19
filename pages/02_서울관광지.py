import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="외국인이 좋아하는 서울 관광지 Top 10", layout="wide")

st.title("🗺️ 외국인 관광객 선호 서울 명소 TOP 10")
st.subheader("마커 위에 마우스를 올리면 가장 가까운 지하철역이 표시됩니다.")

# 2. 서울 주요 관광지 10곳 데이터 (위도, 경도, 가까운 지하철역, 놀거리)
tourist_spots = [
    {
        "name": "경복궁 (Gyeongbokgung Palace)",
        "lat": 37.5796, "lon": 126.9770,
        "subway": "3호선 경복궁역 (도보 5분)",
        "activities": "한복 대여 후 무료 입장하기, 수문장 교대식 관람, 고즈넉한 궁궐 산책 및 사진 촬영."
    },
    {
        "name": "명동 거리 (Myeong-dong Street)",
        "lat": 37.5635, "lon": 126.9846,
        "subway": "4호선 명동역 / 2호선 을지로입구역 (도보 2분)",
        "activities": "길거리 음식 탐방(닭꼬치, 떡갈비 등), K-뷰티 화장품 및 패션 쇼핑, 활기찬 야시장 구경."
    },
    {
        "name": "N서울타워 (N Seoul Tower)",
        "lat": 37.5512, "lon": 126.9882,
        "subway": "4호선 명동역에서 남산케이블카 이용 (도보/버스 연계)",
        "activities": "남산 케이블카 타기, 사랑의 자물쇠 걸기, 전망대에서 서울 도심 파노라마 야경 감상."
    },
    {
        "name": "북촌한옥마을 (Bukchon Hanok Village)",
        "lat": 37.5826, "lon": 126.9833,
        "subway": "3호선 안국역 (도보 10분)",
        "activities": "실제 주민들이 거주하는 전통 한옥 골목길 걷기, 전통 찻집에서 차 마시기, 공방 체험."
    },
    {
        "name": "홍대 거리 (Hongdae Street)",
        "lat": 37.5567, "lon": 126.9235,
        "subway": "2호선/공항철도 홍대입구역 (도보 3분)",
        "activities": "거리 버스킹(댄스, 인디 음악) 관람, 이색 테마 카페 방문, 트렌디한 클럽 및 밤문화 체험."
    },
    {
        "name": "인사동 문화거리 (Insadong Street)",
        "lat": 37.5744, "lon": 126.9875,
        "subway": "3호선 안국역 / 5호선 종로3가역 (도보 3분)",
        "activities": "한국 전통 기념품(지필묵, 골동품) 쇼핑, 쌈지길 나선형 건물 구경, 갤러리 미술 전시 관람."
    },
    {
        "name": "동대문 디자인 플라자 (DDP)",
        "lat": 37.5665, "lon": 127.0092,
        "subway": "2, 4, 5호선 동대문역사문화공원역 (연결됨)",
        "activities": "자하 하디드가 설계한 우주선 모양 유기적 건축물 감상, 디자인 전시회 관람, 동대문 패션타운 쇼핑."
    },
    {
        "name": "광장시장 (Gwangjang Market)",
        "lat": 37.5701, "lon": 126.9997,
        "subway": "1호선 종로5가역 / 2, 5호선 을지로4가역 (도보 2분)",
        "activities": "넷플릭스에 나온 유명 칼국수 시식, 빈대떡, 육회, 마약김밥 등 한국 전통 시장 먹거리 올킬."
    },
    {
        "name": "롯데월드타워 & 서울스카이 (Lotte World Tower)",
        "lat": 37.5126, "lon": 127.1025,
        "subway": "2, 8호선 잠실역 (연결됨)",
        "activities": "세계 6위 높이 전망대(서울스카이) 유리바닥 걷기, 대형 쇼핑몰 탐방 및 석촌호수 산책."
    },
    {
        "name": "강남 코엑스몰 & 별마당도서관 (COEX Mall)",
        "lat": 37.5113, "lon": 127.0596,
        "subway": "2호선 삼성역 / 9호선 봉은사역 (연결됨)",
        "activities": "인스타그램 명소인 거대 별마당 도서관에서 인증샷 찍기, 아쿠아리움 관람 및 몰링(Malling)."
    }
]

# 3. 지도 레이아웃과 설명판을 분리하기 위해 컬럼 배치
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗺️ 서울 주요 관광지 지도")
    
    # 서울 중심부 좌표로 초기 지도 생성
    m = folium.Map(location=[37.555, 126.985], zoom_start=12)
    
    # 지도에 관광지 마커 추가
    for spot in tourist_spots:
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=folium.Popup(f"<b>{spot['name']}</b><br>{spot['subway']}", max_width=300),
            # 마우스 오버 시 지하철역이 바로 보이도록 tooltip 설정
            tooltip=f"ℹ️ {spot['name']} - 가장 가까운 역: {spot['subway']}",
            # 노란색 마커 아이콘 지정
            icon=folium.Icon(color="darktoggle", icon="star", icon_color="yellow")
        ).add_to(m)
        
    # 스트림릿에 폴리움 지도 렌더링
    st_folium(m, width="100%", height=550)

with col2:
    st.markdown("### 📌 퀵 내비게이션")
    st.write("지도의 노란색 스타(🌟) 마커를 클릭하시면 상세 정보 팝업창을 보실 수 있습니다. 마우스를 올리면 지하철역 힌트가 나타나요!")
    st.info("💡 팁: 도심권(경복궁, 명동, 북촌 등)은 서로 지하철로 10~15분 내외 거리에 촘촘히 모여 있습니다.")

---

# 4. 지도 하단 관광지별 가이드 정보 제공
st.markdown("---")
st.markdown("## 📋 서울 주요 관광지 10곳 상세 안내 (지하철 및 놀거리)")

# 가독성을 높이기 위해 2열 격자 형태로 하단 설명 배치
info_cols = st.columns(2)

for i, spot in enumerate(tourist_spots):
    # 0, 2, 4.. 번은 1열에 / 1, 3, 5.. 번은 2열에 배치
    with info_cols[i % 2]:
        st.markdown(f"### {i+1}. {spot['name']}")
        st.markdown(f"* **🚇 가까운 지하철역:** {spot['subway']}")
        st.markdown(f"* **🎯 주요 놀거리 & 추천 활동:** {spot['activities']}")
        st.markdown("<br>", unsafe_allow_html=True)
