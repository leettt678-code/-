# app.py
import streamlit as st
from streamlit-folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top 10 - Map (Folium)", layout="wide")

st.title("🌸 서울 외국인 인기 관광지 Top 10 (Folium 지도)")
st.markdown(
    "서울을 방문하는 외국인들에게 인기 있는 명소 10곳을 지도와 함께 소개합니다. "
    "지도에서 마커를 클릭하면 각 장소의 설명을 볼 수 있습니다."
)

# 중심 좌표: 서울
SEOUL_CENTER = (37.5665, 126.9780)

# Top10 장소 (이름, 위도, 경도, 설명, 전철역)
places = [
    {
        "rank": 1,
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.580467,
        "lon": 126.976944,
        "desc": "조선의 대표 궁궐로, 광화문과 근정전이 유명합니다.",
        "station": "경복궁역 (3호선)"
    },
    {
        "rank": 2,
        "name": "Changdeokgung Palace (창덕궁 & 비원)",
        "lat": 37.579254,
        "lon": 126.992150,
        "desc": "유네스코 세계유산으로 지정된 고궁으로, 후원이 특히 아름답습니다.",
        "station": "안국역 (3호선)"
    },
    {
        "rank": 3,
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.582178,
        "lon": 126.983256,
        "desc": "조용한 한옥 골목길과 전통문화체험이 가능한 마을입니다.",
        "station": "안국역 (3호선)"
    },
    {
        "rank": 4,
        "name": "N Seoul Tower (N서울타워 / 남산타워)",
        "lat": 37.551170,
        "lon": 126.988228,
        "desc": "서울 전경을 한눈에 볼 수 있는 전망대로, 야경이 특히 아름답습니다.",
        "station": "명동역 (4호선)"
    },
    {
        "rank": 5,
        "name": "Myeongdong (명동 쇼핑거리)",
        "lat": 37.560000,
        "lon": 126.985800,
        "desc": "쇼핑, 패션, 화장품, 길거리음식이 즐비한 외국인 관광 1번지.",
        "station": "명동역 (4호선)"
    },
    {
        "rank": 6,
        "name": "Insadong (인사동)",
        "lat": 37.574165,
        "lon": 126.984910,
        "desc": "전통찻집, 공예품, 기념품 가게가 모여 있는 거리입니다.",
        "station": "안국역 (3호선)"
    },
    {
        "rank": 7,
        "name": "Hongdae (홍대 거리)",
        "lat": 37.555280,
        "lon": 126.923330,
        "desc": "젊은이의 거리로 예술과 음악, 카페, 거리공연이 가득합니다.",
        "station": "홍대입구역 (2호선, 공항철도)"
    },
    {
        "rank": 8,
        "name": "Dongdaemun Design Plaza (동대문 DDP)",
        "lat": 37.566300,
        "lon": 127.009000,
        "desc": "미래지향적 건축물과 디자인 전시, 야간 LED 장미정원으로 유명합니다.",
        "station": "동대문역사문화공원역 (2·4·5호선)"
    },
    {
        "rank": 9,
        "name": "Gwangjang Market (광장시장)",
        "lat": 37.570977,
        "lon": 126.998944,
        "desc": "빈대떡과 육회비빔밥으로 유명한 서울 전통시장입니다.",
        "station": "종로5가역 (1호선)"
    },
    {
        "rank": 10,
        "name": "Yeouido Hangang Park (여의도 한강공원)",
        "lat": 37.527730,
        "lon": 126.932970,
        "desc": "한강변을 따라 산책, 자전거, 야경을 즐길 수 있는 도심 속 공원입니다.",
        "station": "여의나루역 (5호선)"
    },
]

# Folium Map 생성 (색깔 지도 + 마커 클러스터)
m = folium.Map(location=SEOUL_CENTER, zoom_start=12, tiles="CartoDB positron")
mc = MarkerCluster().add_to(m)

for p in places:
    popup_html = f"""
    <div style="font-family:Arial;">
      <h4 style="margin-bottom:6px;">{p['rank']}. {p['name']}</h4>
      <p style="margin:0;">{p['desc']}</p>
      <p style="margin:0;"><b>가까운 전철역:</b> {p['station']}</p>
    </div>
    """
    folium.Marker(
        location=(p["lat"], p["lon"]),
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{p['rank']}. {p['name']}",
        icon=folium.Icon(color="pink", icon="info-sign")
    ).add_to(mc)

# 지도 출력 (80% 크기)
st.markdown("### 🗺️ 서울 관광 명소 지도")
st_folium(m, width=800, height=520)  # 지도 크기 80% 정도로 축소

# 관광지 소개 목록
st.markdown("---")
st.markdown("### 📍 관광지 간단 소개 & 전철역 안내")
for p in places:
    st.markdown(
        f"**{p['rank']}. {p['name']}** — {p['desc']}  \n🚇 **가까운 전철역:** {p['station']}"
    )

st.markdown("---")
st.caption("데이터 출처: VisitSeoul, TripAdvisor, Klook 등 (지도 좌표는 참고용)")
