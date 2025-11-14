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

def gradient_colors(n):
    red = "#ff4136"
    blue = "#1f77b4"
    white = "#ffffff"

    colors = []
    if n >= 1:
        colors.append(red)

    blue_rgb = hex_to_rgb(blue)
    white_rgb = hex_to_rgb(white)

    for i in range(n - 1):
        t = (i / max(1, n - 2)) * 0.9
        light_rgb = blend(blue_rgb, white_rgb, t)
        colors.append(rgb_to_hex(light_rgb))

    return colors

# 앱
st.title("🌍 Country MBTI Explorer")
st.write("국가를 선택하면 MBTI 비율을 인터랙티브 막대그래프로 보여줍니다.")

df = load_data()
mbti_cols = [c for c in df.columns if c != "Country"]

st.sidebar.header("옵션")
country = st.sidebar.selectbox("국가 선택", df["Country"].sort_values())
sort_flag = st.sidebar.checkbox("값 기준 정렬(내림차순)", True)
show_raw = st.sidebar.checkbox("원본 데이터 보기")

row = df[df["Country"] == country]
ser = row.iloc[0][mbti_cols].astype(float)

chart_df = ser.reset_index()
chart_df.columns = ["MBTI", "Value"]

if sort_flag:
    chart_df = chart_df.sort_values("Value", ascending=False)

colors = gradient_colors(len(chart_df))
color_map = {mbti: colors[i] for i, mbti in enumerate(chart_df["MBTI"])}

chart_df["Pct"] = chart_df["Value"] * 100

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

if show_raw:
    st.subheader("원본 수치 (%)")
    tmp = chart_df[["MBTI", "Pct"]].copy()
    tmp["Pct"] = tmp["Pct"].round(4).astype(str) + "%"
    st.dataframe(tmp)

csv = chart_df[["MBTI", "Value"]].to_csv(index=False)
st.download_button(
    "CSV 다운로드",
    data=csv,
    file_name=f"{country}_MBTI.csv",
    mime="text/csv",
)
