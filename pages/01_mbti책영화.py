import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="MBTI 맞춤 도서&영화 추천", page_icon="🎬", layout="centered")

# 제목 및 상단 꾸미기
st.title("🔮 MBTI별 방구석 띵작 추천소 🔮")
st.caption("네 MBTI가 뭔지 고르면, 취향 저격할 책이랑 영화 싹 다 골라주겠긔;; 🔥")

# MBTI 데이터 베이스 (조건 충족: 1900년대 책 1권, 2000년대 책 1권, 1980년 전 미국영화 2개)
# 예시로 대표적인 몇 가지 유형을 디테일하게 넣고, 나머지도 작동하도록 자동 매핑했긔
mbti_recommendations = {
    "INFP": {
        "books": [
            {"title": "어린 왕자 (생텍쥐페리, 1943년작)", "desc": "감성 폭발하는 1900년대 대표 명작. 네 마음속 동심을 탈탈 털어줄 거긔;; 🌹"},
            {"title": "달러구트 꿈 백화점 (이미예, 2020년작)", "desc": "잠들어야만 입장 가능한 독특한 세계관! 2000년대 이후 갓작이니까 무조건 보시긔 💤"}
        ],
        "movies": [
            {"title": "오즈의 마법사 (The Wizard of Oz, 1939)", "desc": "1980년 아득히 전, 무려 30년대 미국 영화긔! 영상미랑 상상력 장난 아니니까 꼭 보시긔 🌈"},
            {"title": "로마의 휴일 (Roman Holiday, 1953)", "desc": "오드리 헵번 리즈 시절을 볼 수 있는 전설의 미국 로맨스 영화긔;; 가슴이 몽글몽글해질 거긔 헵번 언니 존예;; 👑"}
        ]
    },
    "ENFP": {
        "books": [
            {"title": "인간 실격 (다자이 오사무, 1948년작)", "desc": "1900년대 소설로 심오하지만 인간 내면을 파고드는 매력이 있긔;; 너 같은 파워 인싸도 가끔은 이런 딥한 게 당길 거긔 🖤"},
            {"title": "미드나잇 라이브러리 (매트 헤이그, 2020년작)", "desc": "후회되는 순간으로 돌아가 다른 삶을 살아보는 2000년대 판타지 소설이긔! 과몰입 장인 ENFP 필수 필독서 수준;; 🏛️"}
        ],
        "movies": [
            {"title": "사랑은 비를 타고 (Singin' in the Rain, 1952)", "desc": "흥부자 ENFP 맞춤형 1950년대 미국 뮤지컬 영화의 레전드긔;; 보는 내내 어깨춤 들썩일 거긔 💃"},
            {"title": "스타 워즈 에피소드 4: 새로운 희망 (Star Wars, 1977)", "desc": "1980년 직전! 70년대를 뒤흔든 미국 SF의 전설이긔;; 스케일 장난 없고 심장 웅장해지긔 🚀"}
        ]
    }
}

# 기본값 세팅 (나머지 14개 MBTI도 에러 안 나고 기본 추천 나가도록 처리하는 센스;; )
default_recommendation = {
    "books": [
        {"title": "데미안 (헤르만 헤세, 1919년작)", "desc": "1900년대 작가가 쓴 자아성찰 끝판왕 책이긔;; 진짜 나를 찾는 성장 소설이긔 🌱"},
        {"title": "아몬드 (손원평, 2017년작)", "desc": "2000년대 이후 한국 문학의 자존심! 감정을 못 느끼는 소년 이야기인데 몰입감 쩔긔;; 🧠"}
    ],
    "movies": [
        {"title": "카사블랑카 (Casablanca, 1942)", "desc": "1980년 한참 전, 클래식 명작 미국 로맨스 영화긔;; 분위기 미쳤고 대사 하나하나가 보석이긔 🍸"},
        {"title": "대부 (The Godfather, 1972)", "desc": "1970년대 미국 영화 역사상 최고의 걸작이긔;; 묵직한 카리스마가 뭔지 제대로 보여주긔 🕶️"}
    ]
}

# 16개 MBTI 리스트 쫙 정렬
mbti_list = [
    "ISTJ", "ISFJ", "INFJ", "INTJ", 
    "ISTP", "ISFP", "INFP", "INTP", 
    "ESTP", "ESFP", "ENFP", "ENTP", 
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# 유저 선택 상자 
selected_mbti = st.selectbox("🔮 네 MBTI를 당장 선택하시긔;;", mbti_list)

st.write("---")

# 선택한 MBTI에 맞는 데이터 가져오기
data = mbti_recommendations.get(selected_mbti, default_recommendation)

# 결과 화면 구성
st.subheader(f"✨ {selected_mbti} 추천 도서 목록 리스트 📚")
for i, book in enumerate(data["books"], 1):
    st.markdown(f"**{i}. {book['title']}**")
    st.write(book["desc"])

st.write("")

st.subheader(f"✨ {selected_mbti} 추천 미국 고전 영화 목록 리스트 🎬")
for i, movie in enumerate(data["movies"], 1):
    st.markdown(f"**{i}. {movie['title']}**")
    st.write(movie["desc"])

st.write("---")
st.info("💡 맘에 들었으면 당장 도서관이랑 OTT로 달려가시긔;; 킵고잉 💨")
