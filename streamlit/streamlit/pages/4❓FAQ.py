import streamlit as st
import pandas as pd

# 데이터베이스 연결
conn = st.connection("mydb", type='sql', autocommit=True)

# SQL 쿼리로 데이터 가져오기
sql = """
    SELECT 
        q.question_id,
        q.company_id,
        q.question,
        q.answer,
        c.company_name
    FROM company_faq q
    JOIN company c ON q.company_id = c.company_id
   ORDER BY q.company_id ASC
"""

df = conn.query(sql, ttl=360)

# CSS 스타일 정의
st.markdown("""
    <style>
    .small-text {
        font-size: 12px;
    }
    .question {
        font-size: 20px;
        color: #2e8b57;
        margin-bottom: 10px;
    }
    .answer {
        font-size: 16px;
        color: #4682b4;
    }
    .divider {
        border-bottom: 1px solid #ccc;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 스트림릿 앱 인터페이스
st.title("❓ 자주 하는 질문 FAQ")
st.markdown(
    """
    <br/>
    """,
    unsafe_allow_html=True
)
# 검색 입력
query = st.text_input(" 궁금하신 키워드를 입력하세요 ! ")

#st.markdown('<div class="small-text"> 계약금   |   납기일   |   장애인차량   |   수리</div>', unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .small-text {
        font-size: 12px;
    }
    .small-text span {
        margin-right: 30px; 
    }
    </style>
    <div class="small-text">
        <span>계약금</span>
        <span>|</span>
        <span>납기일</span>
        <span>|</span>
        <span>장애인차량</span>
        <span>|</span>
        <span>수리</span>
        <span>|</span>
        <span>포인트</span>
        <span>|</span>
        <span>판매</span>
    </div>
    <br/>
    <br/>

    """,
    unsafe_allow_html=True
)

# 검색 엔진 함수
def search_keywords(df, query):
    if query:
        results = df[df['question'].str.contains(query, case=False, na=False)]
    else:
        results = df  # 검색어가 없을 경우 모든 데이터를 반환
    return results

# 검색 결과 필터링
filtered_df = search_keywords(df, query)

# 회사별로 데이터 분류
companies = filtered_df['company_id'].unique()

# 탭 이름 설정
try : 
    tab_names = [filtered_df[filtered_df['company_id'] == company]['company_name'].iloc[0] for company in companies]
    tabs = st.tabs(tab_names)

# 질문 뽑아내기
    for i, company in enumerate(companies):
        with tabs[i]:
            st.header(tab_names[i])
            
            company_data = filtered_df[filtered_df['company_id'] == company]
            
            for _, row in company_data.iterrows():
                with st.expander(f"{row['question']}"):
                    st.markdown(f"<div class='divider'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='answer'>{row['answer']}</div>", unsafe_allow_html=True)
except :
    st.write("입력하신 키워드에 해당하는 내용이 없습니다.")

