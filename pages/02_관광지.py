# app.py
import streamlit as st
from streamlit_folium import st_folium
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

# Top10 장소 데이터
places = [
    (1, "Gyeongbokgung Palace (경복궁)", 37.580467, 126.976944,
     "조선의 대표 궁궐로, 광화문과 근정전이 유명합니다.", "경복궁역 (3호선)"),
    (2, "Changdeokgung Palace (창덕궁 & 비원)", 37.579254, 126.992150,
     "유네스코 세계유산으로 지정된 고궁으로, 후원이 특히 아름답습니다.", "안국역 (3호선)"),
    (3, "Bukchon Hanok Village (북촌한옥마을)", 37.582178, 126.983256,
     "조용한 한옥 골목길과 전통문화체험이 가능한 마을입니다.", "안국역 (3호선)"),
    (4, "N Seoul Tower (남산타워)", 37.551170, 126.988228,
     "서울 전경을 한눈에 볼 수 있는 전망대로, 야경이 특히 아름답습니다.", "명동역 (4호선)"),
    (5, "Myeongdong (명동 쇼핑거리)", 37.560000, 126.985800,
     "쇼핑, 패션, 화장품, 길거리음식이 즐비한 외국인 관광 1번지.", "명동역 (4호선)"),
    (6, "Insadong (인사동)", 37.574165, 126.984910,
     "전통찻집, 공예품, 기념품 가게가 모여 있는 거리입니다.", "안국역 (3호선)"),
    (7, "Hongdae (홍대 거리)", 37.555280, 126.923330,
     "젊은이의 거리로 예술과 음악, 카페, 거리공연이 가득합니다.", "홍대입구역 (2호선, 공항철도)"),
    (8, "Dongdaemun Design Plaza (동대문 DDP)", 37.566300, 127.009000,
     "미래지향적 건축물과 디자인 전시, 야간 LED 장미정원으로 유명합니다.", "동대문역사문화공원역 (2·4·5호선)"),
    (9, "Gwangjang Market (광장시장)", 37.570977, 126.998944,
     "빈대떡과 육회비빔밥으로 유명한 서울 전통시장입니다.", "종로5가역 (1호선)"),
    (10, "Yeouido Hangang Park (여의도 한강공원)", 37.527730, 126.932970,
     "한강변을 따라 산책, 자전거, 야경을 즐길 수 있는 도심 속 공원입니다.", "여의나루역 (5호선)")
]

# 지도 생성
m = folium.Map(location=SEOUL_CENTER, zoom_start=12, tiles="CartoDB positron")
mc = MarkerCluster().add_to(m)

for rank, name, lat, lon, desc, station in places:
    popup_html = (
        "<div style='font-family:Arial;'>"
        "<h4 style='margin-bottom:6px;'>"
        "{rank}. {name}</h4>"
        "<p style='margin:0;'>{desc}</p>"
        "<p style='margin:0;'><b>가까운 전철역:</b> {station}</p>"
        "</div>"
    ).format(rank=rank, name=name, desc=desc, station=station)

    folium.Marker(
        location=(lat, lon),
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{rank}. {name}",
        icon=folium.Icon(color="pink", icon="info-sign")
    ).add_to(mc)

# 지도 출력 (80% 크기)
st.markdown("### 🗺️ 서울 관광 명소 지도")
st_folium(m, width=800, height=520)

# 관광지 간단 소개
st.markdown("---")
st.markdown("### 📍 관광지 간단 소개 & 전철역 안내")
for rank, name, lat, lon, desc, station in places:
    st.markdown(
        f"**{rank}. {name}** — {desc}  \n🚇 **가까운 전철역:** {station}"
    )

st.markdown("---")
st.caption("데이터 출처: VisitSeoul, TripAdvisor, Klook 등 (지도 좌표는 참고용)")
