import streamlit as st
import pandas as pd

###Sample################################################################################
# 데이터 예제
data_brand = {
    "순위": [1, 2, 3, 4, 5, 6],
    "brand": ["현대", "기아", "제네시스", "KGM", "르노코리아", "쉐보레"],
    "판매량": [47700, 44284, 12104, 4102, 2041, 1869],
    "점유율": ["42.6%", "39.5%", "10.8%", "3.7%", "1.8%", "1.7%"],
    "작년 대비": [4264, 1827, 1968, 101, 140, 448],
    "모델 별 판매": [52064, 46111, 10136, 4001, 1901, 2317],
    "모델 별 증가": [56325, 51138, 13838, 5758, 1721, 5141]
}

data_model = {
    "순위": [1, 2, 3, 4, 5, 6],
    "모델": ["카니발", "쏘렌토", "스포티지", "쏘나타 디 엣지", "디 올 뉴 그랜저", "셀토스"],
    "판매량": [47700, 44284, 12104, 4102, 2041, 1869],
    "점유율": ["42.6%", "39.5%", "10.8%", "3.7%", "1.8%", "1.7%"],
    "작년 대비": [4264, 1827, 1968, 101, 140, 448],
    "모델 별 판매": [52064, 46111, 10136, 4001, 1901, 2317],
    "모델 별 증가": [56325, 51138, 13838, 5758, 1721, 5141]
}

data_hyundai= {
    "순위": [1, 2, 3, 4, 5, 6],
    "모델": ["디 올 뉴 싼타페", "더 뉴 투싼", "포터2", "더 뉴 아반뗴", "디 올 뉴 그랜저", "캐스퍼"],
    "판매량": [47700, 44284, 12104, 4102, 2041, 1869],
    "점유율": ["42.6%", "39.5%", "10.8%", "3.7%", "1.8%", "1.7%"],
    "작년 대비": [4264, 1827, 1968, 101, 140, 448],
    "모델 별 판매": [52064, 46111, 10136, 4001, 1901, 2317],
    "모델 별 증가": [56325, 51138, 13838, 5758, 1721, 5141]
}

data_kia = {
    "이미지": ["https://autoimg.danawa.com/photo/4466/model_200.png","","","","",""],
    "순위": [1, 2, 3, 4, 5, 6],
    "모델": ["쏘렌토", "카니발", "스포티지", "레이", "셀토스", "K5"],
    "판매량": [47700, 44284, 12104, 4102, 2041, 1869],
    "점유율": ["42.6%", "39.5%", "10.8%", "3.7%", "1.8%", "1.7%"],
    "작년 대비": [4264, 1827, 1968, 101, 140, 448],
    "모델 별 판매": [52064, 46111, 10136, 4001, 1901, 2317],
    "모델 별 증가": [56325, 51138, 13838, 5758, 1721, 5141]
}

brands = { "hyundai" : "./streamlit/res/hyundai.png",
            "kia" : "./streamlit/res/kia.png",
            "kgm" : "./streamlit/res/kgm.png",
            "genesis" : "./streamlit/res/genesis.png"
        }
##########################################################################################
def create_brand_link(df):
    df['company_name'] = df.apply(lambda row: f'<a href="/?brand={row["company_name"]}" target="_self">{row["company_name"]}</a>', axis=1)
    return df

##########################################################################################\
# URL 파라미터 읽기
# try:
#     st.session_state.selected_brand = st.query_params["brand"]
# except KeyError:
#     st.session_state.selected_brand = 'hyundai'




# Streamlit 애플리케이션 제목
st.title('🚗국산차 랭킹 ~순위~')

df_brand = pd.DataFrame(data_brand)
df_model = pd.DataFrame(data_model)

#selected_brand = "현대"

# HTML과 CSS를 사용하여 더 진하고 굵은 구분선을 추가
st.markdown(
    """
    <hr style="border: 2px solid black;">
    """,
    unsafe_allow_html=True
)        

# 추가적인 기능들
tab_brand, tab_model = st.tabs(["브랜드별", "모델별"])

data_editor_column_config = {
    "브랜드": st.column_config.LinkColumn(),
    "이미지" : st.column_config.ImageColumn(),
    "순위": st.column_config.Column(disabled=True),
    "모델": st.column_config.LinkColumn(),
    "판매량": st.column_config.Column(disabled=True),
    "점유율": st.column_config.Column(disabled=True),
    "작년 대비": st.column_config.Column(disabled=True),
    "모델 별 판매": st.column_config.Column(disabled=True),
    "모델 별 증가": st.column_config.Column(disabled=True)
}


#############################################################################
st.session_state.selected_name = 'hyundai'

with tab_brand:
    #st.write("브랜드별 데이터를 보여줍니다.")
    df_brand = create_brand_link(df_brand)
    #st.data_editor(df_brand, column_config = data_editor_column_config, hide_index=True)
    st.write(df_brand.to_html(escape=False, index=False), unsafe_allow_html=True)


with tab_model:
    # 이미지 버튼 생성
    cols = st.columns(len(brands))

    for i, name in enumerate(brands.keys()):
        with cols[i]:
            if st.button(name):
                st.session_state.selected_name = name
            st.image("https://discord.com/channels/1263684182962602087/1263684182962602090/1265497319282049137")
    st.write("모델별 데이터를 보여줍니다.")
    
    #데이터 선택에 맞게 변경
    if st.session_state.selected_name == 'hyundai':
        data_model = data_hyundai
    else:
        data_model = data_kia

    df_model = pd.DataFrame(data_model)
    st.data_editor(df_model, column_config = data_editor_column_config, hide_index=True)