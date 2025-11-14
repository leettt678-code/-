import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Country MBTI Explorer", layout="wide")

@st.cache_data
def load_data(path="/mnt/data/countriesMBTI_16types.csv"):
    df = pd.read_csv(path)
    cols = [c for c in df.columns if c != "Country"]
    return df[["Country"] + cols]

# 색상 유틸
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def blend(c1, c2, t):
    return tuple(int((1 - t) * c1[i] + t * c2[i]) for i in range(3))

def gradient(n, start="#1f77b4"):
    # 파란색 → 흰색 그라데이션 n개
    base = hex_to_rgb(start)
    white = hex_to_rgb("#ffffff")
    colors = []
    for i in range(n):
        t = (i / max(1, n - 1)) * 0.8
        colors.append(rgb_to_hex(blend(base, white, t)))
    return colors

############################################
# APP START
############################################

df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

st.title("🌍 Country MBTI Explorer")
tab1, tab2 = st.tabs(["국가별 분석", "MBTI 유형별 분석"])

############################################
# TAB 1 — 국가별 MBTI 분석
############################################
with tab1:
    st.subheader("국가 선택 → MBTI 비율 분석")

    country = st.selectbox("국가 선택", df["Country"].sort_values())

    row = df[df["Country"] == country]
    ser = row.iloc[0][mbti_cols].astype(float)

    chart_df = ser.reset_index()
    chart_df.columns = ["MBTI", "Value"]
    chart_df = chart_df.sort_values("Value", ascending=False).reset_index(drop=True)
    chart_df["Pct"] = chart_df["Value"] * 100

    # 색 (1등 = 빨강, 나머지 파랑 그라데이션)
    colors = ["#ff4136"] + gradient(len(chart_df) - 1)
    color_map = {chart_df["MBTI"][i]: colors[i] for i in range(len(chart_df))}

    fig = px.bar(
        chart_df,
        x="MBTI",
        y="Pct",
        text="Pct",
        color="MBTI",
        color_discrete_map=color_map,
        title=f"{country} — MBTI 비율 (%)",
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_yaxes(range=[0, chart_df["Pct"].max() * 1.2])
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

############################################
# TAB 2 — MBTI 유형별 국가 TOP 10
############################################
with tab2:
    st.subheader("MBTI 유형 선택 → 해당 유형 비율이 높은 국가 Top 10")

    mbti = st.selectbox("MBTI 유형 선택", mbti_cols)

    # 정렬 후 Top10
    top10 = df[["Country", mbti]].sort_values(mbti, ascending=False).head(10)
    top10["Pct"] = top10[mbti] * 100

    # 색: 한국(Korea, Republic of / South Korea 포함 시) → 빨강
    korea_names = ["South Korea", "Korea, Republic of", "Korea"]
    bars = top10["Country"].tolist()

    bar_colors = []
    for c in bars:
        if any(k in c for k in korea_names):
            bar_colors.append("#ff4136")   # 한국 빨간색
        else:
            bar_colors.append(None)         # 나중에 채움

    # 나머지 파랑 그라데이션 채우기
    blue_grad = gradient(bar_colors.count(None))
    idx = 0
    for i in range(len(bar_colors)):
        if bar_colors[i] is None:
            bar_colors[i] = blue_grad[idx]
            idx += 1

    fig2 = px.bar(
        top10,
        x="Country",
        y="Pct",
        text="Pct",
        title=f"{mbti} 유형이 가장 높은 국가 Top 10",
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        marker_color=bar_colors,
    )
    fig2.update_yaxes(range=[0, top10["Pct"].max() * 1.2])

    st.plotly_chart(fig2, use_container_width=True)

