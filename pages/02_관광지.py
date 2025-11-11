import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlit 설정
st.set_page_config(page_title="서울 관광지 Top10 (외국인 인기)", layout="wide")

st.title("🇰🇷 외국인들이 사랑하는 서울 관광지 Top 10")
st.markdown("서울의 대표 관광지 10곳을 Folium 지도 위에 표시합니다.")

# 서울 주요 관광지 데이터
PLACES = [
    ("경복궁 (Gyeongbokgung Palace)", 37.579884, 126.9768, "조선시대의 대표 궁궐"),
    ("창덕궁 (Changdeokgung Palace)", 37.57944, 126.99278, "유네스코 지정 세계유산, 후원이 유명"),
    ("북촌한옥마을 (Bukchon Hanok Village)", 37.582178, 126.983255, "전통 한옥이 밀집된 골목길"),
    ("인사동 (Insadong)", 37.574551, 126.983795, "전통 찻집, 공예품 상점, 외국인 인기 지역"),
    ("명동 (Myeongdong)", 37.564, 126.985, "쇼핑과 길거리 음식의 중심지"),
    ("남산타워 (N Seoul Tower)", 37.55117, 126.988228, "서울 전경을 한눈에 볼 수 있는 전망대"),
    ("동대문시장 (Dongdaemun Market)", 37.563275, 126.995238, "패션 도매, 24시간 쇼핑 가능"),
    ("광장시장 (Gwangjang Market)", 37.570, 126.999, "한국 전통 음식과 재래시장"),
    ("홍대거리 (Hongdae Area)", 37.55094, 126.93559, "젊음의 거리, 예술과 음악의 중심"),
    ("롯데월드타워 (Lotte World Tower)", 37.5126, 127.1025, "초고층 전망대와 쇼핑몰")
]

# Folium 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles="OpenStreetMap")

# 마커 추가
for name, lat, lon, desc in PLACES:
    folium.Marker(
        [lat, lon],
        tooltip=name,
        popup=f"<b>{name}</b><br>{desc}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Heatmap 옵션
st.sidebar.header("지도 설정")
use_heatmap = st.sidebar.checkbox("관광지 밀집도 보기 (Heatmap)", value=False)

if use_heatmap:
    try:
        from folium.plugins import HeatMap
        HeatMap([[lat, lon] for _, lat, lon, _ in PLACES], radius=25).add_to(m)
    except Exception as e:
        st.sidebar.error("HeatMap 로드 실패: " + str(e))

# Folium 지도 출력
st_folium(m, width=1100, height=700)

st.divider()
st.subheader("📍 관광지 정보")
for i, (name, lat, lon, desc) in enumerate(PLACES, 1):
    st.write(f"{i}. **{name}** — {desc}  \n   위치: ({lat}, {lon})")
