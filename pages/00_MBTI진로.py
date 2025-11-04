import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 진로 추천기 🎯", page_icon="🎓", layout="centered")

# 제목
st.title("🎓 MBTI로 알아보는 나의 진로 추천 💡")
st.write("안녕! 😊 너의 MBTI를 골라봐~ 그러면 딱 맞는 진로를 추천해줄게!")

# MBTI 리스트
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 선택박스
mbti = st.selectbox("👉 너의 MBTI는 뭐야?", ["선택 안 함"] + mbti_list)

# MBTI별 추천 진로
careers = {
    "INTJ": ["데이터 과학자 📊", "전략 기획자 🧠"],
    "INTP": ["연구원 🔬", "소프트웨어 개발자 💻"],
    "ENTJ": ["기업가 💼", "경영 컨설턴트 📈"],
    "ENTP": ["마케팅 기획자 📢", "창업가 🚀"],
    "INFJ": ["상담사 💬", "작가 ✍️"],
    "INFP": ["디자이너 🎨", "심리상담가 🧘‍♀️"],
    "ENFJ": ["교사 👩‍🏫", "HR 매니저 🤝"],
    "ENFP": ["크리에이터 🎥", "기획자 🎯"],
    "ISTJ": ["회계사 📚", "공무원 🏛️"],
    "ISFJ": ["간호사 🩺", "사회복지사 🤗"],
    "ESTJ": ["프로젝트 매니저 📅", "경영자 🧱"],
    "ESFJ": ["교사 👩‍🏫", "홍보 담당자 📣"],
    "ISTP": ["엔지니어 ⚙️", "기술 전문가 🔧"],
    "ISFP": ["예술가 🎭", "패션 디자이너 👗"],
    "ESTP": ["세일즈 전문가 💬", "이벤트 플래너 🎉"],
    "ESFP": ["연예인 🎤", "엔터테이너 🌟"]
}

# 추천 출력
if mbti != "선택 안 함":
    st.subheader(f"✨ {mbti} 유형에게 어울리는 진로는...")
    rec1, rec2 = careers[mbti]
    st.write(f"1️⃣ {rec1}")
    st.write(f"2️⃣ {rec2}")
    st.success("이 진로들이 너의 강점을 제대로 살려줄 거야! 💪🔥")
else:
    st.info("위에서 MBTI를 선택해줘 😄")

# 하단 문구
st.write("---")
st.caption("💡 만든이: ChatGPT | 청소년을 위한 진로 추천 서비스 🎯")
