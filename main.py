1. import streamlit as st
st.title('나의 첫 웹 서비스 만들기')
a=st.text_input('왓츠 유얼 네임?')
b=st.selectbox('좋아하는 사람을 초이스하세요!', ['김진성','양예성','윤희성'])
if st.button('인삿말 생성')
  st.write(a+님, 헬로우~!')
