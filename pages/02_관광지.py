# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top 10 - Map (Folium)", layout="wide")

st.title("서울 외국인 인기 관광지 Top 10 — 지도 표시 (Folium)")
st.markdown(
    "맵의 마커를 클릭하면 각 장소 이름과 간단한 설명이 표시됩니다. "
    "이 앱은 Streamlit Cloud(또는 로컬)에서 실행 가능합니다."
)

# 중심 좌표: 서울
SEOUL_CENTER = (37.5665, 126.9780)

# Top10 장소 (이름, 위도, 경도, 간단 설명)
places = [
    {
        "rank": 1,
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.580467,
        "lon": 126.976944,
        "desc": "조선의 대표 궁궐 — 근정전, 광화문 주변."
    },
    {
        "rank": 2,
        "name": "Changdeokgung Palace (창덕궁 & 비원)",
        "lat": 37.579254,
        "lon": 126.992150,
        "desc": "유네스코 세계유산 - 비원(후원)으로 유명."
    },
    {
        "rank": 3,
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.582178,
        "lon": 126.983256,
        "desc": "전통 한옥이 남아있는 보행형 마을(주거지역이니 예의준수)."
    },
    {
        "rank": 4,
        "name": "N Seoul Tower (N서울타워 / 남산타워)",
        "lat": 37.551170,
        "lon": 126.988228,
        "desc": "서울 전경을 한눈에 — 야경과 전망대가 인기."
    },
    {
        "rank": 5,
        "name": "Myeongdong (명동 쇼핑거리)",
        "lat": 37.560000,
        "lon": 126.985800,
        "desc": "쇼핑과 스트리트푸드의 메카, 화장품·패션 상점 밀집."
    },
    {
        "rank": 6,
        "name": "Insadong (인사동)",
        "lat": 37.574165,
        "lon": 126.984910,
        "desc": "전통 공예와 찻집, 기념품 골목."
    },
    {
        "rank": 7,
        "name": "Hongdae / Hongik Univ. Area (홍대)",
        "lat": 37.555280,
        "lon": 126.923330,
        "desc": "젊음의 거리, 예술·라이브클럽·카페가 유명."
    },
    {
        "rank": 8,
        "name": "Dongdaemun Design Plaza (동대문 DDP)",
        "lat": 37.566300,
        "lon": 127.009000,
        "desc": "자하 하디드 설계의 디자인 랜드마크, 야간 라이트 업 인기."
    },
    {
        "rank": 9,
        "name": "Gwangjang Market (광장시장)",
        "lat": 37.570977,
        "lon": 126.998944,
        "desc": "전통 시장 + 길거리 음식(빈대떡, 비빔밥 등) — 먹거리 추천."
    },
    {
        "rank": 10,
        "name": "Yeouido Hangang Park (여의도 한강공원)",
        "lat": 37.527730,
        "lon": 126.932970,
        "desc": "한강변 공원, 자전거·피크닉·야경(63빌딩 근처)."
    },
]

# 사이드바: 체크박스로 표시할 장소 필터링
st.sidebar.header("표시할 장소 선택")
show_all = st.sidebar.checkbox("모두 표시", value=True)
selected_ranks = None
if not show_all:
    # 사용자가 보고 싶은 랭크 선택(멀티 셀렉트)
    choices = [f"{p['rank']}. {p['name']}" for p in places]
    selected = st.sidebar.multiselect("표시할 장소를 선택하세요", choices, default=choices[:5])
    # 선택된 랭크 번호 파싱
    selected_ranks = [int(s.split(".")[0]) for s in selected]

# Folium Map 생성
m = folium.Map(location=SEOUL_CENTER, zoom_start=12, tiles="OpenStreetMap")

# 마커 추가 (클러스터)
from folium.plugins import MarkerCluster
mc = MarkerCluster().add_to(m)

for p in places:
    if (not show_all) and (p["rank"] not in selected_ranks):
        continue
    popup_html = f"""
    <div style="font-family:Arial;">
      <h4 style="margin-bottom:6px;">{p['rank']}. {p['name']}</h4>
      <p style="margin:0;">{p['desc']}</p>
    </div>
    """
    folium.Marker(
        location=(p["lat"], p["lon"]),
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{p['rank']}. {p['name']}"
    ).add_to(mc)

# 지도 출력
st.markdown("### 지도 (클릭해서 더보기)")
map_data = st_folium(m, width="100%", height=650)

# 장소 리스트 출력
st.markdown("---")
st.markdown("### Top 10 장소 (목록)")
for p in places:
    if (not show_all) and (p["rank"] not in selected_ranks):
        continue
    st.write(f"**{p['rank']}. {p['name']}** — {p['desc']}  \n위치: {p['lat']}, {p['lon']}")

st.markdown("---")
st.caption("데이터 출처: VisitSeoul, TripAdvisor, Klook 등 (지도 표시는 참고용 좌표).")
