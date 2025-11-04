import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천기 🎯", page_icon="🎓")

st.title("🎓 MBTI로 알아보는 나의 진로 추천 💡")
st.write("안녕! 😊 너의 MBTI를 골라봐~ 그러면 딱 맞는 진로를 추천해줄게!")

mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("👉 너의 MBTI는 뭐야?", mbti_list)

# MBTI별 진로 추천 데이터
careers = {
    "INTJ": ["데이터 과학자 📊", "전략 기획자 🧠"],
    "INTP": ["연구원 🔬", "소프트웨어 개발자 💻"],
    "ENTJ": ["기업가 💼", "경영 컨설턴트 📈"],
    "ENTP": ["마케팅 기획자 📢", "창업가 🚀"],
    "INFJ": ["상담사 💬", "작가 ✍️"],
    "INFP":
