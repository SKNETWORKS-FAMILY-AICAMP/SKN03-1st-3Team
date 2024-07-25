import streamlit as st

st.title('차량 구매 효율성을 위한 모델 및 브랜드 정보와 FAQ')
# st.page_link("index.py", label="Home", icon="🏠")
st.page_link("./pages/char.py", label="Why⁉️ 전국 자동차 등록 증감률", icon="1️⃣")
st.page_link("./pages/ranking_brand_st.py", label="브랜드별 랭킹", icon="2️⃣")
st.page_link("./pages/ranking_model_st.py", label="모델별 랭킹", icon="3️⃣")
st.page_link("./pages/ranking_brand_st.py", label="FAQ", icon="4️⃣")
st.page_link("https://auto.danawa.com/", label="다나와", icon="🌎")