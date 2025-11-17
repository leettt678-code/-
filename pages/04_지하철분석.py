import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np
import os

# -------------------------------
# 데이터 로드
# -------------------------------
@st.cache_data
def load_data():
    # 현재 파일이 pages에 있기 때문에 상위 폴더의 CSV를 불러와야 함
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "..", "subway.csv")

    df = pd.read_csv(csv_path, encoding="cp949")
    df["사용일자"] = pd.to_datetime(df["사용일자"], format="%Y%m%d")
    return df

df = load_data()

# -------------------------------
# UI
# -------------------------------
st.title("📊 2025년 10월 지하철 승·하차 TOP10 분석")
st.write("날짜와 호선을 선택하면 승·하차 인원이 가장 많은 10개 역을 보여줍니다.")

# 날짜 선택
selected_date = st.date_input(
    "날짜 선택",
    value=date(2025, 10, 1),
    min_value=date(2025, 10, 1),
    max_value=date(2025, 10, 31)
)

# 호선 선택
lines = sorted(df["노선명"].unique())
selected_line = st.selectbox("호선 선택", lines)

# -------------------------------
# 데이터 필터링
# -------------------------------
filtered = df[
    (df["사용일자"] == pd.Timestamp(selected_date)) &
    (df["노선명"] == selected_line)
].copy()

if filtered.empty:
    st.warning("⚠️ 해당 날짜와 호선에 대한 데이터가 없습니다.")
    st.stop()

filtered["승하차합계"] = filtered["승차총승객수"] + filtered["하차총승객수"]

# TOP 10 추출
top10 = filtered.sort_values("승하차합계", ascending=False).head(10)

# -------------------------------
# 색상 설정
# 1위 = 빨간색, 나머지 = 파란색 → 흐려지는 그라데이션
# -------------------------------
colors = ["red"]  # 1위

blue_start = np.array([0, 0, 255])      # 진한 파란색
blue_end = np.array([200, 220, 255])    # 흐린 파란색

gradient = [
    f"rgb({int(c[0])}, {int(c[1])}, {int(c[2])})"
    for c in [
        blue_start + (blue_end - blue_start) * i
        for i in np.linspace(0, 1, len(top10) - 1)
    ]
]

colors.extend(gradient)

# -------------------------------
# 그래프 생성 (Plotly)
# -------------------------------
fig = go.Figure()
fig.add_trace(go.Bar(
    x=top10["역명"],
    y=top10["승하차합계"],
    marker=dict(color=colors),
    text=top10["승하차합계"],
    textposition="outside"
))

fig.update_layout(
    title=f"🚇 {selected_date} | {selected_line} 승·하차 총합 TOP10",
    xaxis_title="역명",
    yaxis_title="승·하차 인원",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
