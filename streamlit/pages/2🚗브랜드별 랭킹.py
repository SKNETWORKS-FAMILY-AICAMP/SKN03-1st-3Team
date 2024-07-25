import streamlit as st

# 커넥션 객체 생성
conn = st.connection("mydb", type = "sql",autocommit=True)

data_editor_column_config = {
    "브랜드": st.column_config.Column(),
    "이미지" : st.column_config.ImageColumn(),
    "순위": st.column_config.Column(disabled=True),
    "모델": st.column_config.LinkColumn(),
    "판매량": st.column_config.Column(disabled=True),
    "점유율": st.column_config.NumberColumn(disabled=True, format="%d%%"),
    "작년 대비": st.column_config.Column(disabled=True),
    "전월 판매량": st.column_config.Column(disabled=True),
    "전월 대비 증가량": st.column_config.Column(disabled=True),
    "모델 별 판매": st.column_config.Column(disabled=True),
    "모델 별 증가": st.column_config.Column(disabled=True)
}

st.title('🚗 국산차 브랜드별 랭킹 순위')
st.divider()

#st.page_link("./pages/3🚕모델별 랭킹.py", label="모델별")

selected_month = st.selectbox(
        " ",
        ("2024년 %0d월"%i for i in range(1,7,1))
    )

sql = """
    select
        ROW_NUMBER()over(order by sales_volume desc) as '순위'
        , company_logo as '이미지'
        , company_name '브랜드'
        , sales_volume '판매량'
        , company_share '점유율'
        , company_month_over_month '전월 판매량'
        , company_salse_by_month '전월 대비 증가량'
    from company c 
    inner join company_vehicle cv
        on c.company_id = cv.company_id
    where cv.company_date= '2024-%02d'
    order by sales_volume desc
    ;
    """ % int(selected_month.replace('월','').replace('2024년 ',''))
print(sql)
df = conn.query(sql, ttl= 3600)
st.dataframe(df, column_config = data_editor_column_config, hide_index=True, use_container_width=True)