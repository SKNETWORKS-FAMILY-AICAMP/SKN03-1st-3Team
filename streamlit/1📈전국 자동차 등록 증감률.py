import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# 데이터베이스 연결
conn = st.connection("mydb", type='sql', autocommit=True)

# SQL 쿼리로 데이터 가져오기
sql = """
    SELECT 
           year
         , official
         , commercial
         , private
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
    plt.plot(df['year'], df[f'{column}_증감율'], marker='o', label=column)

plt.xlabel('Year')
plt.ylabel('Rate(%)')
#plt.title('연도별 자동차 등록 증감율 비교')
plt.legend()
plt.grid(True)

# Streamlit을 통해 그래프 표시
st.pyplot(plt)

st.write("전국 자동차 등록 현황 데이터를 이용하여 연도별로 증감율을 비교했습니다.\n" 
        "관용, 영업용,승용을 비교했을 때 승용의 증감율이 가장 큰 폭으로 상승하고 있는 것을 보아\n"
        "일반 사용자의 수요가 증가하고 있음을 알 수 있습니다.\n"
        "따라서 저희는 일반 사용자가 보다 편리하게 차량을 구매할 수 있도록 서비스를 제공하고자 합니다.")