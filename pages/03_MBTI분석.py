import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="세계 MBTI 분석", layout="wide")

# CSV 파일 불러오기
@st.cache_data
def load_data():
    # pages 폴더 → 상위폴더로 이동 후 CSV 파일 읽기
    path = os.path.join(os.path.dirname(__file__), "..", "countriesMBTI_16types.csv")
    return pd.read_csv(path)

df = load_data()

st.title("🌏 세계 MBTI 비율 분석")


# -----------------------------
# Tabs 생성
# -----------------------------
tab1, tab2 = st.tabs(["📊 전체 데이터", "🧬 MBTI 유형별 분석"])


# =============================
# TAB 1 : 전체 테이블
# =============================
with tab1:
    st.subheader("전체 국가 MBTI 비율 데이터")
    st.dataframe(df)


# =============================
# TAB 2 : MBTI 유형별 분석
# =============================
with tab2:
    st.subheader("MBTI 유형별로 국가별 비율 상위 10개 비교")

    mbti_list = [col for col in df.columns if col not in ["Country"]]

    selected_type = st.selectbox("MBTI 유형 선택", mbti_list)

    # 비율 높은 순으로 정렬
    top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

    # 한국 강조 색상 지정
    colors = ["red" if c == "Korea" or c == "South Korea" else "gray" for c in top10["Country"]]

    # Matplotlib 그래프
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top10["Country"], top10[selected_type], color=colors)
    ax.set_title(f"{selected_type} 비율 상위 10개 국가")
    ax.set_ylabel("Percentage (%)")
    ax.set_xticklabels(top10["Country"], rotation=45, ha="right")

    st.pyplot(fig)

    st.markdown("🔴 한국은 빨간색으로 표시됩니다.")


