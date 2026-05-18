import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('왓츠 유얼 네임?')
b=st.selectbox('좋아하는 사람을 초이스하세요!', ['김진짜 (김진성)','양 (양예성)','윤상큼 (윤희성)'])
if st.button('인삿말 생성'):
  st.write(a+'님, 헬로우~!')
  st.info('웰컴~')
  st.warning(b+'이라는 친구를 좋아하시나봐요~ㅎ.ㅎ')
  st.error('잘 부탁합니듀')
  st.balloons()
