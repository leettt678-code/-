import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="세계 MBTI 분석", layout="wide")

# ===================================================
# 데이터 불러오기
# ===================================================
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "..", "countriesMBTI_16types.csv")
    return pd.read_csv(path)

df = load_data()

st.title("🌏 세계 MBTI 비율 분석")


# ===================================================
# Tabs
# ===================================================
tab1, tab2, tab3 = st.tabs([
    "📁 전체 데이터",
    "📊 국가별 MBTI 비율",
    "🏆 MBTI 유형별 TOP 10 국가"  # ▶▶ 새로 추가한 탭
])


# ===================================================
# TAB 1: 전체 데이터 보기
# ===================================================
with tab1:
    st.subheader("전체 국가 MBTI 비율 데이터")
    st.dataframe(df)


# ===================================================
# TAB 2: 특정 국가의 16개 MBTI 비율 그래프
# ===================================================
with tab2:
    st.subheader("국가를 선택하면 MBTI 16유형 비율을 보여줍니다.")

    country = st.selectbox("국가 선택", df["Country"].unique())

    row = df[df["Country"] == country].squeeze()

    mbti_cols = [c for c in df.columns if c != "Country"]
    values = row[mbti_cols].values

    # 상위 1등은 빨강, 나머지 파란 계열
    sorted_idx = values.argsort()[::-1]
    colors = []
    for i, idx in enumerate(sorted_idx):
        if i == 0:
            colors.append("red")
        else:
            blue_intensity = 0.1 + (0.9 * (1 - i / len(sorted_idx)))
            colors.append((0, 0.3, blue_intensity))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar([mbti_cols[i] for i in sorted_idx], [values[i] for i in sorted_idx], color=colors)
    ax.set_title(f"{country} 의 MBTI 비율")
    ax.set_ylabel("Percentage (%)")
    ax.set_xticklabels([mbti_cols[i] for i in sorted_idx], rotation=45, ha="right")

    st.pyplot(fig)


# ===================================================
# TAB 3: MBTI 유형 기준 TOP10 국가 그래프 (한국은 빨간색)
# ===================================================
with tab3:
    st.subheader("MBTI 유형을 선택하면 해당 유형 비율이 높은 국가 TOP 10을 보여줍니다.")
    
    mbti_list = [c for c in df.columns if c != "Country"]
    selected_type = st.selectbox("MBTI 유형 선택", mbti_list)

    # 선택한 유형 기준 상위 10개 국가
    top10 = df[["Country", selected_type]].sort_values(by=selected_type, ascending=False).head(10)

    # 색상: 한국만 빨간색
    colors = ["red" if c.lower() in ["korea", "south korea"] else "gray" for c in top10["Country"]]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top10["Country"], top10[selected_type], color=colors)
    ax.set_title(f"{selected_type} 비율 상위 10개 국가")
    ax.set_ylabel("Percentage (%)")
    ax.set_xticklabels(top10["Country"], rotation=45, ha="right")

    st.pyplot(fig)

    st.markdown("🔴 한국(Korea, South Korea)은 자동으로 빨간색으로 표시됩니다.")
