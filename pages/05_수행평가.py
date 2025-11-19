import os
import streamlit as st
import pandas as pd
import plotly.express as px
import urllib.request
import json
from collections import Counter

st.set_page_config(page_title="부산 안내문자 통계 & 지도", layout="wide")
st.title("📊 부산광역시 구별 안내문자 통계 & 지도")

# -------------------------
# 1) CSV 파일 경로 (pages 폴더 -> 상위 루트의 CSV)
# -------------------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "gagagaga.CSV")

if not os.path.exists(CSV_PATH):
    st.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}\n(루트에 gagagaga.CSV가 있는지 확인하세요)")
    st.stop()

# CSV는 cp949(윈도우 한글) 형식일 가능성이 있어 cp949로 읽습니다
try:
    df = pd.read_csv(CSV_PATH, encoding="cp949")
except Exception as e:
    st.error(f"CSV 로드 오류: {e}")
    st.stop()

st.markdown(f"**데이터 로드 완료** — 전체 행: {len(df)}")

# -------------------------
# 2) 대상지역 파싱 (콤마로 분리) -> '구/군' 단위로 세기
# -------------------------
if "대상지역" not in df.columns:
    st.error("CSV에 '대상지역' 컬럼이 없습니다. 컬럼명을 확인해 주세요.")
    st.stop()

# 부산의 행정 구/군 리스트 (일반적 명칭)
BUSAN_GU_LIST = [
    "중구","서구","동구","영도구","부산진구","동래구","남구","북구","해운대구",
    "사하구","금정구","강서구","연제구","수영구","사상구","기장군"
]

def normalize_gu(name: str) -> str:
    """구 이름 정규화: 공백 제거, '구'/'군' 형태 유지 (예: '해운대구')"""
    if not isinstance(name, str):
        return ""
    s = name.strip()
    # 일부 항목에 괄호나 공백이 섞여있을 수 있어 간단 정리
    s = s.replace(" ", "").replace("　", "")
    # 만약 '부산광역시'가 포함되면 제거
    s = s.replace("부산광역시", "")
    return s

# 대상지역 칼럼에서 모든 구를 뽑아 카운트
all_gu = []
for val in df["대상지역"].dropna().astype(str):
    # 쉼표 기준으로 분리
    parts = [p.strip() for p in val.split(",") if p.strip() != ""]
    for p in parts:
        p_norm = normalize_gu(p)
        # 후보가 BUSAN_GU_LIST에 있거나 '구' 혹은 '군' 문자열을 포함하면 채택
        if p_norm in BUSAN_GU_LIST:
            all_gu.append(p_norm)
        else:
            # 일부 데이터는 '부산광역시'만 있거나 '구'가 생략된 케이스가 있을 수 있음
            # 끝에 '구' 혹은 '군'이 포함된다면 그대로 사용
            if p_norm.endswith("구") or p_norm.endswith("군"):
                all_gu.append(p_norm)
            else:
                # 혹은 '기장'처럼 '군'이 빠진 경우 '기장군'으로 보정 시도
                if p_norm in ["기장"]:
                    all_gu.append("기장군")
                # 그 외는 무시

# 집계
gu_counter = Counter(all_gu)

# 결과 DataFrame (빈 구도 모두 표시)
result_df = pd.DataFrame({
    "구": BUSAN_GU_LIST,
    "안내문자수": [gu_counter.get(g, 0) for g in BUSAN_GU_LIST]
})

# 정렬: 안내문자수 내림차순
result_df = result_df.sort_values("안내문자수", ascending=False).reset_index(drop=True)

st.subheader("📌 구별 안내문자 집계")
st.dataframe(result_df)

# -------------------------
# 3) 색 지정: max=red, min=blue, others=yellow
# -------------------------
max_idx = result_df["안내문자수"].idxmax()
min_idx = result_df["안내문자수"].idxmin()
max_gu = result_df.loc[max_idx, "구"]
min_gu = result_df.loc[min_idx, "구"]

def pick_color(gu):
    if gu == max_gu:
        return "red"
    elif gu == min_gu:
        return "blue"
    else:
        return "yellow"

result_df["color"] = result_df["구"].apply(pick_color)

# -------------------------
# 4) Plotly 막대그래프 (인터랙티브)
# -------------------------
st.subheader("📊 막대그래프: 구별 안내문자수")
fig_bar = px.bar(
    result_df,
    x="구",
    y="안내문자수",
    color="color",
    color_discrete_map="identity",  # color 컬럼의 값(red/blue/yellow)을 그대로 사용
    text="안내문자수",
    title="부산광역시 구별 안내문자 수"
)
fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(yaxis_title="안내문자 수", xaxis_title="구", height=520)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------
# 5) 지도 시각화 (Plotly Choropleth Mapbox)
# -------------------------
st.subheader("🗺 지도 시각화 (부산 구별)")

GEOJSON_URL = "https://raw.githubusercontent.com/juminemap/geojson_korea/master/municipalities/geojson/부산광역시.geojson"

try:
    with urllib.request.urlopen(GEOJSON_URL) as url:
        geojson = json.loads(url.read().decode())
except Exception as e:
    st.error(f"GeoJSON을 불러오는 데 실패했습니다: {e}")
    st.stop()

# GeoJSON 내부 feature의 지역명 키가 무엇인지 확정하기 위해 시도적으로 추출
# 각 feature의 properties에서 가능한 이름을 찾아 정규화한 값을 새 속성 'gu_norm'에 넣습니다.
def extract_best_name(props: dict) -> str:
    # 후보 키들 (데이터마다 다를 수 있으므로 여러 키 시도)
    candidate_keys = ["name", "NAME", "adm_nm", "SIG_KOR_NM", "name_kor", "county", "EMD_KOR_NM", "CTP_KOR_NM"]
    for k in candidate_keys:
        if k in props and isinstance(props[k], str) and props[k].strip() != "":
            return props[k]
    # 마지막으로 properties 전체를 문자열화 시도
    for v in props.values():
        if isinstance(v, str) and v.strip() != "":
            return v
    return ""

# 각 feature에 'gu_norm' 속성 추가 (정규화)
for feat in geojson.get("features", []):
    props = feat.get("properties", {})
    raw_name = extract_best_name(props)
    # 정규화: 공백 제거, '구'/'군' 등 유지
    raw_name = raw_name.replace(" ", "").replace("　", "")
    # 일부 소스는 "부산광역시 중구" 같은 형식일 수 있으니 '부산' 제거
    raw_name = raw_name.replace("부산광역시", "").replace("부산", "")
    # 마지막 확인: 만약 이름이 'Jung-gu' 영문 등이라면 소문자로 변환 (보완)
    feat["properties"]["gu_norm"] = raw_name

# 이제 result_df에도 동일 방식의 정규화 컬럼 추가
result_df["gu_norm"] = result_df["구"].str.replace(" ", "").str.replace("　", "")

# 확인: 어떤 geojson feature gu_norm이 우리 result_df와 매칭되는지 보장하기 위해
# (일치하지 않으면 지도에 표시되지 않을 수 있음 — 이 경우 이름 매핑을 추가로 조정해야 함)
available_geo_names = {feat["properties"].get("gu_norm", "") for feat in geojson.get("features", [])}
matched = result_df["gu_norm"].isin(available_geo_names).sum()
if matched == 0:
    st.warning("지도와 구 이름 매칭이 되지 않았습니다. GeoJSON의 지역명 구조가 다른 것 같습니다. (아래는 시도한 정규화 결과)")
    st.write("GeoJSON에 존재하는 예시 지역명:", list(sorted(list(available_geo_names)))[0:10])
else:
    st.write(f"지도 매칭된 구 수: {matched} / {len(result_df)}")

# 지도용 컬러: max=red, min=blue, others=yellow
result_df["map_color"] = result_df["color"]  # 이미 red/blue/yellow

# Plotly Choropleth (categorical color)
fig_map = px.choropleth_mapbox(
    result_df,
    geojson=geojson,
    locations="gu_norm",
    featureidkey="properties.gu_norm",
    color="map_color",
    color_discrete_map={"red":"red","blue":"blue","yellow":"yellow"},
    hover_name="구",
    hover_data={"안내문자수":True, "gu_norm":False, "map_color":False},
    mapbox_style="carto-positron",
    center={"lat": 35.1796, "lon": 129.0756},
    zoom=9.6,
    opacity=0.7,
    title="부산광역시 구별 안내문자 수 (색: 최대=빨강, 최소=파랑, 기타=노랑)"
)

fig_map.update_layout(height=700, margin={"r":0,"t":50,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# -------------------------
# 6) 다운로드 / 요약
# -------------------------
st.subheader("요약")
st.markdown(f"- 총 메시지(행) 수: **{len(df)}**")
st.markdown(f"- 구별 집계 상위 3:\n{result_df.head(3).to_csv(index=False)}")

st.success("완료 — 필요하면 '날짜 필터', '키워드 분석', '시계열' 등 추가 기능을 더해드릴게요.")
