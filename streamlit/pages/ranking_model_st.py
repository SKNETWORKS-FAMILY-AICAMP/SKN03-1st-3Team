import streamlit as st

# 커넥션 객체 생성
conn = st.connection("mydb", type = "sql",autocommit=True)

st.session_state.selected_name = "현대"

data_editor_column_config = {
    "브랜드": st.column_config.LinkColumn(),
    "브랜드이미지" : st.column_config.ImageColumn(),
    "순위": st.column_config.Column(disabled=True),
    "모델": st.column_config.LinkColumn(),
    "모델이미지": st.column_config.ImageColumn(),
    "판매량": st.column_config.Column(disabled=True),
    "점유율": st.column_config.NumberColumn(disabled=True, format="%d%%"),
    "작년 대비": st.column_config.Column(disabled=True),
    "전월": st.column_config.Column(disabled=True),
    "전월 대비 증가량": st.column_config.Column(disabled=True),
    "모델 별 판매": st.column_config.Column(disabled=True),
    "모델 별 증가": st.column_config.Column(disabled=True)
}

st.title('🚗2024 국산차 랭킹 ~순위~')
st.divider()


st.page_link("./pages/ranking_brand_st.py", label="브랜드별")

selected_month = st.selectbox(
        "모델 별 데이터를 조회 할 월을 선택해주세요",
        ("%0d월"%i for i in range(1,7,1))
    )

sql = """
    select 
           company_logo 
         , company_name 
      from company c 
     where 1=1
       and company_name in ('현대', '기아', '제네시스')
     order by company_name asc
    ;
"""
company_df = conn.query(sql, ttl= 3600)

cols = st.columns(len(company_df))
i=0
print(company_df)
for company in company_df.itertuples():
    print(company)
    with cols[i]:
            if st.button(company[2]):
                st.session_state.selected_name = company[2]
            st.image(company[1])
    i+=1

sql = """
      select 
  		    ROW_NUMBER()over(order by sales_volume desc) as '순위'
  	   , c.company_logo as '브랜드이미지'
  	   , c.company_name as '브랜드'
  	   , m.model_img  as '모델이미지'
  	   , m.model_name  as '모델'
  	   , mv.sales_volume as '판매량'
       , mv.model_share as '점유율'
  	   , mv.model_month_over_month as '전월 판매량'
       , model_salse_by_month '전월 대비 증가량'
    from company c 
   inner join model_vehicle mv 
      on c.company_id = mv.company_id 
   inner join model m
      on mv.model_id = m.model_id 
   where mv.model_date = '2024-%02d'
     and company_name = '%s'
   order by sales_volume desc
    ;
    """ % (int(selected_month.replace('월','')), st.session_state.selected_name)

df = conn.query(sql, ttl= 3600)
st.dataframe(df, column_config = data_editor_column_config, hide_index=True, use_container_width=True)