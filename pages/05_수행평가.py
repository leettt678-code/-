import streamlit as st
import pandas as pd
import plotly.express as px
import json
import urllib.request
import os

st.set_page_config(page_title="부산 안내문자 통계 + 지도", layout="wide")

st.title("📊 부산광역시 구별 안내문자 통계 + 지도 시각화")
st.write("업로드한 CSV 자료를 기반으로 구별 안내문자 수를 집계하고 지도 시각화를 제공합니다.")

# -------------------------
# 1. CSV 파일 로드
# -------------------------

file_path = "/mnt/data/busanjaenanmunja.CSV"

if not os.path.exists(file_path):
    st.error("CSV 파일을 찾을 수 없습니다. Streamlit Cloud 업로드 상태를 확인하세요.")
    st.stop()

df = pd.read_csv(file_path, encoding="utf-8")

# -------------------------
# 2. 구 컬럼 자동 탐지
# -------------------------
gu_cols = [c for c in df.columns if "구" in c]

if len(gu_cols) == 0:
    st.error("데이터 안에 '구'가 들어간 컬럼을 찾지 못했습니다.")
    st.stop()

gu_col = gu_cols[0]
st.info(f"자동 감지된 구 컬럼: **{gu_col}**")

# -------------------------
# 3. 구별 집계
# -------------------------
gu_count = df[gu_col].value_counts().reset_index()
gu_count.columns = ["구", "안내문자수"]

# -------------------------
# 4. 색 지정
# -------------------------
max_gu = gu_count.loc[gu_count["안내문자수"].idxmax(), "구"]
min_gu = gu_count.loc[gu_count["안내문자수"].idxmin(), "구"]

def color_map(gu):
    if gu == max_gu:
        return "red"
    elif gu == min_gu:
        return "blue"
    return "yellow"

gu_count["color"] = gu_count["구"].apply(color_map)

st.subheader("📌 구별 안내문자 수")
st.dataframe(gu_count)

# -------------------------
# 5. Plotly 막대 그래프
# -------------------------

fig_bar = px.bar(
    gu_count,
    x="구",
    y="안내문자수",
    color="color",
    color_discrete_map="identity",
    text="안내문자수",
    title="부산광역시 구별 안내문자 수 (Bar Chart)"
)

fig_bar.update_traces(textposition='outside')
fig_bar.update_layout(height=500)

st.subheader("📊 구별 안내문자 수 (막대그래프)")
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# 6. 부산광역시 구 경계 GeoJSON 불러오기
# -------------------------
geojson_url = "https://raw.githubusercontent.com/juminemap/geojson_korea/master/municipalities/geojson/부산광역시.geojson"

with urllib.request.urlopen(geojson_url) as url:
    geojson_data = json.loads(url.read().decode())

# -------------------------
# 7. Choropleth 지도 시각화
# -------------------------

# 구 이름을 GeoJSON와 맞추기 위해 소문자 정규화
gu_count["구_normalized"] = gu_count["구"].str.replace(" ", "").str.replace("구", "").str.lower()

fig_map = px.choropleth_mapbox(
    gu_count,
    geojson=geojson_data,
    locations="구_normalized",
    featureidkey="properties.name_eng",  # geojson의 영어 이름 대응
    color="안내문자수",
    mapbox_style="carto-positron",
    zoom=9.8,
    center={"lat": 35.1796, "lon": 129.0756},
    opacity=0.6,
    title="🗺 부산광역시 구별 안내문자 수 (지도 시각화)"
)

fig_map.update_layout(height=650)

st.subheader("🗺 지도 시각화 (Choropleth Map)")
st.plotly_chart(fig_map, use_container_width=True)
