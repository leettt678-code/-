import streamlit as st
st.title('우거지 해장국과 실존하는 진우')
name=st.text_input('이름을 입력하세요:')
if st.button('인사말 생성'):
  st.info(name+'님! 안녕하세요')
  st.warning('반가워요')
  st.balloons()
