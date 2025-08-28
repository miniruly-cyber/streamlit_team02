# 파일명: education_ui.py
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="교육 앱 UI 샘플", layout="wide")

# ---------------------------
# 검색창
# ---------------------------
st.header("강의 검색")
search_query = st.text_input("검색어 입력", "")

# ---------------------------
# 추천 강의
# ---------------------------
st.subheader("추천 강의")
cols = st.columns(3)
for i, col in enumerate(cols):
    col.image("https://via.placeholder.com/150", caption=f"추천 강의 {i+1}")
    col.write("강의 제목 예시")
    col.progress(i*30+10)
    col.button("수강하기", key=f"enroll{i}")

# ---------------------------
# 강의 목록 카드
# ---------------------------
st.subheader("내 강의 목록")
for row in range(2):
    cols = st.columns(3)
    for i, col in enumerate(cols):
        idx = row*3 + i + 1
        col.image("https://via.placeholder.com/120", caption=f"강의 {idx}")
        col.write("진행률: 50%")
        col.button("수강 계속하기", key=f"continue{idx}")

# ---------------------------
# 학습 현황 그래프 (샘플)
# ---------------------------
st.subheader("학습 현황")
import matplotlib.pyplot as plt

modules = ["Module1", "Module2", "Module3"]
progress = [50, 75, 30]

fig, ax = plt.subplots()
ax.bar(modules, progress, color="skyblue")
ax.set_ylabel("진행률 (%)")
st.pyplot(fig)
