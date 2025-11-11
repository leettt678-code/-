# app.py - Streamlit app to show Seoul's top 10 tourist spots (folium map)
# Save this file as app.py and the requirements below as requirements.txt

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Seoul Top10 for Foreigners", layout="wide")
st.title("서울에서 외국인들이 좋아하는 관광지 Top 10 — 지도 표시 (Folium)")
st.markdown("이 앱은 Folium 지도를 사용해 서울의 대표 관광지 10곳을 표시합니다. Streamlit Cloud에서 바로 실행 가능합니다.")

# Top 10 places (name, latitude, longitude, short description)
PLACES = [
    ("Gyeongbokgung Palace (경복궁)", 37.579884, 126.9768, "Joseon 시대의 대표 궁궐. 관광객 필수 코스"),
    ("Changdeokgung Palace (창덕궁)", 37.57944, 126.99278, "유네스코 지정 세계유산. 후원이 유명"),
    ("Bukchon Hanok Village (북촌 한옥마을)", 37.582178, 126.983255, "전통 한옥이 모여 있는 골목 관광지"),
    ("Insadong (인사동)", 37.574551, 126.983795, "전통 공예품, 찻집, 기념품 상점 밀집 지역"),
    ("Myeongdong (명동)", 37.564, 126.985, "쇼핑과 먹거리의 중심지(화장품, 패션)") ,
    ("N Seoul Tower (남산타워)", 37.55117, 126.988228, "서울 전경을 한눈에 볼 수 있는 전망대"),
    ("Dongdaemun Market (동대문)", 37.563275, 126.995238, "24시간 쇼핑 가능, 패션 도매의 중심지"),
    ("Gwangjang Market (광장시장)", 37.570, 126.999, "한국 전통 길거리 음식과 재래시장 경험") ,
    ("Hongdae / Hongik Univ. Area (홍대)", 37.55094, 126.93559, "젊음의 거리, 공연과 카페, 쇼핑"),
    ("Lotte World Tower & Mall (롯데월드타워)", 37.5126, 127.1025, "서울의 초고층 타워, 전망대와 쇼핑몰")
]

# Create folium map centered on Seoul
initial_location = [37.5665, 126.9780]  # approx. center of Seoul (City Hall area)
m = folium.Map(location=initial_location, zoom_start=12)

# Add markers
for name, lat, lon, desc in PLACES:
    popup_html = f"<b>{name}</b><br>{desc}<br><i>좌표: {lat}, {lon}</i>"
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=name,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Fit map to markers
bounds = [[p[1], p[2]] for p in PLACES]
m.fit_bounds(bounds, padding=(30, 30))

st.sidebar.header("지도 옵션")
show_heatmap = st.sidebar.checkbox("관광지 간 열지도(예: 밀집 강조)", value=False)

if show_heatmap:
    try:
        from folium.plugins import HeatMap
        HeatMap([[p[1], p[2]] for p in PLACES], radius=25).add_to(m)
    except Exception as e:
        st.sidebar.error("HeatMap 플러그인 불러오기 실패: " + str(e))

st.header("지도")
# Render folium map in Streamlit
st_data = st_folium(m, width=1100, height=700)

st.markdown("---")
st.subheader("Top 10 관광지 목록")
for i, (name, lat, lon, desc) in enumerate(PLACES, start=1):
    st.write(f"{i}. **{name}** — {desc} (좌표: `{lat}, {lon}`)")

st.markdown("앱을 Streamlit Cloud에 배포하려면 이 파일(app.py)과 아래의 requirements.txt를 GitHub 저장소에 올리고 Streamlit에 연결하세요.")

# End of app

# -------------------------
# requirements.txt 내용 (아래를 별도 파일로 저장하세요)
# -------------------------
# streamlit
# folium
# streamlit-folium
# branca
#
# 선택(고급): pandas
