import os
import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.request
import urllib.parse
import json
from collections import Counter

st.set_page_config(page_title="부산 안내문자 통계 & 지도", layout="wide")
st.title("📊 부산광역시 구별 안내문자 통계 & 지도")


# ------------------------------------------------------------
# 1) CSV 파일 경로 (pages → 상위 루트)
# ------------------------------------------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "gagagaga.CSV")

if not os.path.exists(CSV_PATH):
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")
except:
    df = pd.read_csv(CSV_PATH, encoding="utf-8", errors="ignore")

st.success(f"데이터 로드 완료 — 총 {len(df)}행")


# ------------------------------------------------------------
# 2) 대상지역에서 구/군 이름 파싱
# ------------------------------------------------------------
if "대상지역" not in df.columns:
    st.error("CSV에 '대상지역' 컬럼이 없습니다.")
    st.stop()

BUSAN_GU_LIST = [
    "중구","서구","동구","영도구","부산진구","동래구","남구","북구","해운대구",
    "사하구","금정구","강서구","연제구","수영구","사상구","기장군"
]

def clean_name(x):
    if not isinstance(x, str):
        return ""
    x = x.replace("부산광역시", "").replace(" ", "").replace("　", "")
    return x

all_gu = []
for row in df["대상지역"].dropna():
    items = [i.strip() for i in str(row).split(",") if i.strip() != ""]
    for item in items:
        name = clean_name(item)
        if name in BUSAN_GU_LIST:
            all_gu.append(name)
        else:
            if name.endswith("구") or name.endswith("군"):
                all_gu.append(name)
            elif name == "기장":
                all_gu.append("기장군")

gu_counter = Counter(all_gu)

result_df = pd.DataFrame({
    "구": BUSAN_GU_LIST,
    "안내문자수": [gu_counter.get(g, 0) for g in BUSAN_GU_LIST]
})

result_df = result_df.sort_values("안내문자수", ascending=False).reset_index(drop=True)
st.subheader("📌 구별 안내문자 집계")
st.dataframe(result_df)


# ------------------------------------------------------------
# 3) 색 지정 (최대=red, 최소=blue, 나머지=yellow)
# ------------------------------------------------------------
max_gu = result_df.loc[result_df["안내문자수"].idxmax(), "구"]
min_gu = result_df.loc[result_df["안내문자수"].idxmin(), "구"]

def color_map(gu):
    if gu == max_gu:
        return "red"
    elif gu == min_gu:
        return "blue"
    return "yellow"

result_df["color"] = result_df["구"].apply(color_map)


# ------------------------------------------------------------
# 4) Plotly 막대그래프
# ------------------------------------------------------------
st.subheader("📊 막대그래프")
fig_bar = px.bar(
    result_df,
    x="구",
    y="안내문자수",
    text="안내문자수",
    color="color",
    color_discrete_map="identity",
    title="부산 구별 안내문자 수"
)
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)


# ------------------------------------------------------------
# 5) 지도 시각화 (GeoJSON)
# ------------------------------------------------------------
st.subheader("🗺 지도 시각화")

# 한글 URL 인코딩 처리
RAW_GEOJSON_URL = "https://raw.githubusercontent.com/juminemap/geojson_korea/master/municipalities/geojson/부산광역시.geojson"
GEOJSON_URL = urllib.parse.quote(RAW_GEOJSON_URL, safe=':/')

try:
    with urllib.request.urlopen(GEOJSON_URL) as url:
        geojson = json.loads(url.read().decode("utf-8"))
except Exception as e:
    st.error(f"GeoJSON을 불러오는 데 실패했습니다: {e}")
    st.stop()

# GeoJSON 속성에서 행정구 이름 추출
def extract_name(props):
    for key in ["name", "NAME", "adm_nm", "SIG_KOR_NM", "name_kor"]:
        if key in props:
            return clean_name(props[key])
    for v in props.values():
        if isinstance(v, str):
            return clean_name(v)
    return ""

for feat in geojson["features"]:
    feat["properties"]["gu_norm"] = extract_name(feat["properties"])

result_df["gu_norm"] = result_df["구"].map(clean_name)

fig_map = px.choropleth_mapbox(
    result_df,
    geojson=geojson,
    locations="gu_norm",
    featureidkey="properties.gu_norm",
    color="color",
    color_discrete_map={"red":"red","blue":"blue","yellow":"yellow"},
    hover_name="구",
    hover_data={"안내문자수": True},
    mapbox_style="carto-positron",
    center={"lat": 35.1796, "lon": 129.0756},
    zoom=9.5,
    opacity=0.7,
    title="부산광역시 구별 안내문자 지도"
)

st.plotly_chart(fig_map, use_container_width=True)
