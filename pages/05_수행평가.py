import streamlit as st
import pandas as pd
import os

st.title("데이터 분석 앱 (지도 시각화 제거 버전)")

# -------------------------------
# CSV 로드 (상위 폴더에서)
# -------------------------------
@st.cache_data
def load_data():
    # pages 폴더 기준 상위폴더 → CSV
    csv_path = os.path.join(os.path.dirname(__file__), "..", "gagagaga.CSV")

    if not os.path.exists(csv_path):
        st.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        return None
    
    try:
        df = pd.read_csv(csv_path, encoding="cp949")
        return df
    except Exception as e:
        st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
        return None


df = load_data()

if df is None:
    st.stop()

st.success("CSV 파일 불러오기 완료!")

# -------------------------------
# 데이터 미리보기
# -------------------------------
st.subheader("데이터 미리보기")
st.dataframe(df)

# -------------------------------
# 컬럼 선택 후 기초 통계 보기
# -------------------------------
st.subheader("기초 통계량 보기")
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if len(numeric_cols) > 0:
    col = st.selectbox("통계를 확인할 숫자형 컬럼", numeric_cols)
    st.write(df[col].describe())
else:
    st.info("숫자형 컬럼이 없습니다.")

# -------------------------------
# 문자열 컬럼의 값 개수
# -------------------------------
st.subheader("문자열 컬럼 값 개수 확인")

object_cols = df.select_dtypes(include=["object"]).columns.tolist()
if len(object_cols) > 0:
    col2 = st.selectbox("값 개수를 확인할 컬럼", object_cols)
    st.write(df[col2].value_counts())
else:
    st.info("문자열(object) 컬럼이 없습니다.")
