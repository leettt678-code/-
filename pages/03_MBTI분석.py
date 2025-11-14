# streamlit_mbti_app.py
# Streamlit app to explore MBTI distributions by country using Plotly
# Place this file under your Streamlit app repo (e.g., main app directory or pages/) and
# ensure the CSV is at /mnt/data/countriesMBTI_16types.csv on the environment (Cloud files uploaded).

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from typing import List, Dict, Tuple

st.set_page_config(page_title="Country MBTI Explorer", layout="wide")

@st.cache_data
def load_data(path: str = "/mnt/data/countriesMBTI_16types.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # Ensure consistent column order
    cols = [c for c in df.columns if c != 'Country']
    df = df[['Country'] + cols]
    return df


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def blend_color(c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    # linear blend: t=0 -> c1, t=1 -> c2
    return (int(round((1-t) * c1[0] + t * c2[0])),
            int(round((1-t) * c1[1] + t * c2[1])),
            int(round((1-t) * c1[2] + t * c2[2])))


def make_colors_for_bars(m: int) -> Dict[str, str]:
    # m = number of MBTI types (usually 16)
    # We'll produce a mapping for each MBTI key in descending order: 1st -> red, others -> blue->lighter gradient
    red = '#ff4136'            # 1st place color
    base_blue = '#1f77b4'      # start blue for 2nd place
    white = '#ffffff'
    blue_rgb = hex_to_rgb(base_blue)
    white_rgb = hex_to_rgb(white)

    colors = []
    if m >= 1:
        colors.append(red)
    if m > 1:
        others = m - 1
        # generate gradient for others from base_blue to much lighter (towards white)
        for i in range(others):
            # t goes from 0 (strong blue) to 0.9 (very light) as i increases
            if others == 1:
                t = 0.0
            else:
                t = (i / (others - 1)) * 0.9
            rgb = blend_color(blue_rgb, white_rgb, t)
            colors.append(rgb_to_hex(rgb))
    return colors


# --- App UI ---
st.title("🌍 Country MBTI Explorer — 인터랙티브 차트")
st.markdown("선택한 국가의 MBTI 비율을 인터랙티브한 Plotly 막대그래프로 보여줍니다.")

# Load data
with st.spinner("데이터 로딩 중..."):
    df = load_data()

mbti_cols = [c for c in df.columns if c != 'Country']

# Sidebar controls
st.sidebar.header("컨트롤")
country = st.sidebar.selectbox("국가 선택", df['Country'].sort_values())
sort_by_value = st.sidebar.checkbox("막대 정렬: 비율 기준(내림차순)", value=True)
show_raw = st.sidebar.checkbox("원본 수치표 보기", value=False)

# extract selected country's series
row = df.loc[df['Country'] == country]
if row.empty:
    st.error("선택한 국가의 데이터가 없습니다.")
    st.stop()

ser = row.iloc[0][mbti_cols].astype(float)
chart_df = ser.reset_index()
chart_df.columns = ['MBTI', 'Value']

# Optionally sort
if sort_by_value:
    chart_df = chart_df.sort_values('Value', ascending=False).reset_index(drop=True)
else:
    # keep original MBTI order
    pass

# Build colors mapping: first is red, rest blue->light gradient
colors = make_colors_for_bars(len(chart_df))
# Map each MBTI to color according to the chart_df order
color_map = {mbti: colors[i] for i, mbti in enumerate(chart_df['MBTI'].tolist())}

# Plotly bar chart (show %)
chart_df['Pct'] = chart_df['Value'] * 100

fig = px.bar(chart_df, x='MBTI', y='Pct', text='Pct', title=f"{country} — MBTI 비율", labels={'Pct': '비율 (%)'})
# Apply color mapping
for i, d in enumerate(fig.data):
    # fig.data is a single trace when using px.bar for categorical x; instead we'll set marker colors via a list
    pass
# Instead of manipulating fig.data, recreate with color mapping via color_discrete_map
fig = px.bar(chart_df, x='MBTI', y='Pct', text='Pct', title=f"{country} — MBTI 비율", labels={'Pct': '비율 (%)'},
             color='MBTI', color_discrete_map=color_map)
# Remove legend (not needed for single-category bars)
fig.update_layout(showlegend=False)
# Format text and axes
fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside', hovertemplate='<b>%{x}</b><br>비율: %{y:.2f}%')
fig.update_yaxes(range=[0, max(chart_df['Pct'].max()*1.15, 10)], title_text='비율 (%)')
fig.update_layout(margin=dict(l=40, r=20, t=60, b=40))

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Show raw numbers if requested
if show_raw:
    st.subheader(f"{country} — 원본 비율표")
    st.dataframe(chart_df[['MBTI', 'Value']].assign(Value=lambda d: (d['Value']*100).round(4).astype(str) + '%'))

# Download selected country's MBTI as CSV
csv = chart_df[['MBTI', 'Value']].to_csv(index=False)
st.download_button(label="선택 국가 MBTI CSV 다운로드", data=csv, file_name=f"{country}_MBTI.csv", mime='text/csv')

st.markdown("---")
st.caption("앱: Streamlit + Plotly · 데이터: countriesMBTI_16types.csv")


# ----------------------
# requirements.txt (copy into a requirements.txt in your repo)
# ----------------------
"""
# requirements.txt
streamlit>=1.24
pandas>=2.0
plotly>=5.0
numpy>=1.24
"""
