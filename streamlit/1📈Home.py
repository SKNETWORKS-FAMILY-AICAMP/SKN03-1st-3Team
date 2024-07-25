import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# 데이터베이스 연결
conn = st.connection("mydb", type='sql', autocommit=True)

# SQL 쿼리로 데이터 가져오기
sql = """
    SELECT 
           x.*
    FROM vehicle.annual_vehicle_registrations x
"""

df = conn.query(sql, ttl=360)

# 증감율 계산 함수
def calculate_growth_rate(df, column):
    df[f'{column}_증감율'] = df[column].pct_change() * 100
    return df

# 증감율 계산
for column in ['official', 'commercial', 'private']:
    df = calculate_growth_rate(df, column)

# Streamlit 앱 시작
st.title("📈 전국 자동차 등록 증감율  ")

# 연도별 데이터 테이블 표시
st.subheader("연도별 증감율 그래프")


# 그래프 그리기
plt.figure(figsize=(10, 6))
for column in ['official', 'commercial', 'private']:
    if column == 'private':
        plt.plot(df['year'], df[f'{column}_증감율'], marker='o', label=column, linewidth=3.5, color='red')
    else:
        plt.plot(df['year'], df[f'{column}_증감율'], marker='o', label=column, linewidth=0.5)

plt.xlabel('Year')
plt.ylabel('Rate (%)')
plt.legend()
plt.grid(True)


# Streamlit을 통해 그래프 표시
st.pyplot(plt)

text = """
전국 자동차 등록 현황 데이터를 이용하여 연도별로 전년 대비 증감율을 비교했다.
관용, 영업용, 승용 을 비교했을 때 승용의 경우, 큰 변화 없이 증가율을 띄는 것으로 보아 
수요가 계속해서 상승하고 있음을 알 수 있었다.

따라서 일반 사용자가 보다 편리하게 차량을 구매할 수 있도록 서비스를 제공하고자 한다.
"""
st.text_area("🌠 프로젝트 의의 🌠", text, height=200)