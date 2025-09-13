import streamlit as st
import pandas as pd
import altair as alt
import os

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(page_title="MBTI 국가별 TOP10 시각화", page_icon="🌍", layout="centered")

st.title("🌍 국가별 MBTI 유형 비율 TOP10")
st.markdown("업로드된 데이터를 바탕으로 MBTI 유형별로 **비율이 가장 높은 국가 10개**를 확인할 수 있어요 ✨")

# -----------------------------
# 데이터 불러오기 함수
# -----------------------------
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

data_file = "countriesMBTI_16types.csv"

# -----------------------------
# 데이터 로드
# -----------------------------
if os.path.exists(data_file):
    df = load_data(data_file)
    st.success(f"✅ 기본 데이터 파일을 불러왔습니다: {data_file}")
else:
    uploaded_file = st.file_uploader("📂 데이터 파일을 업로드하세요 (CSV)", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.success("✅ 업로드한 파일을 불러왔습니다.")
    else:
        st.warning("⚠️ 데이터 파일이 필요합니다. CSV 파일을 업로드해주세요.")
        st.stop()

# -----------------------------
# MBTI 유형 리스트
# -----------------------------
mbti_types = ["INFJ","ISFJ","INTP","ISFP","ENTP","INFP","ENTJ","INTJ",
              "ESFP","ESTJ","ENFP","ESTP","ISTJ","ENFJ","ESFJ","ISTP"]

# -----------------------------
# MBTI 선택
# -----------------------------
selected_mbti = st.selectbox("🔎 확인하고 싶은 MBTI 유형을 선택하세요:", mbti_types)

# -----------------------------
# TOP10 국가 추출
# -----------------------------
top10 = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)

# -----------------------------
# Altair 차트 생성
# -----------------------------
chart = (
    alt.Chart(top10)
    .mark_bar(color="teal")
    .encode(
        x=alt.X(selected_mbti, title=f"{selected_mbti} 비율", scale=alt.Scale(domain=[0, top10[selected_mbti].max()*1.1])),
        y=alt.Y("Country", sort="-x", title="국가"),
        tooltip=["Country", selected_mbti]
    )
    .interactive()
)

st.altair_chart(chart, use_container_width=True)

# -----------------------------
# 데이터 테이블 보기 옵션
# -----------------------------
with st.expander("📊 TOP10 데이터 보기"):
    st.dataframe(top10.reset_index(drop=True))

# 푸터
st.markdown("---")
st.caption("✨ 데이터 기반 MBTI 국가 비교 | 만든이: 당신의 AI 도우미 🤖")
