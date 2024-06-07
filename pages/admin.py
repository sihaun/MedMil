import streamlit as st
import os
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from menu import menu_with_redirect
from login import my_data

menu_with_redirect()
plot_label = ['보건소계열', '치과', '일반병원', '한의원/한방병원', '정신병원', '요양병원', '종합병원', '약국']

def fun1(k, data_list):
    for i in range(k):
        data_content = data_list[i]
        st.download_button(
            label=f"{i}번째 clust csv 파일 다운로드",
            data=data_content.to_csv(index=False).encode('cp949'),
            file_name=f'cluster_{i}_data.csv' 
        )

def hos_info():
    with st.form("select_hospital"):
        hospital = st.radio("다운로드 받고자하는 의료기관을 선택하십시오.", plot_label, horizontal=True)
        st.write(hospital, "을(를) 선택하셨습니다.")
        index_hos = plot_label.index(hospital) # 선택한 병원의 인덱스
        k = my_data.get_k(index_hos)
        data_list = []
        button = st.form_submit_button('조회하기')
        if button: 
            data_list = my_data.save_clustered_data(index_hos)
    if button:
        fun1(k, data_list)
    
    

def reserve_count():
    # 방문 횟수 데이터 로드
    sheet_data = pd.read_csv('pages/admin/count.csv', encoding='cp949')
    sheet_data = sheet_data[['의료기관명', '방문 횟수']].sort_values('방문 횟수', ascending=False).reset_index(drop=True)
    # AgGrid를 사용하여 병원의 정보를 표 형태로 표시
    gd = GridOptionsBuilder.from_dataframe(sheet_data)
    gd.configure_selection(selection_mode='single', use_checkbox=False)
    gridoptions = gd.build()
    grid_table = AgGrid(sheet_data, height=800, gridOptions=gridoptions, fit_columns_on_grid_load=True)
    st.download_button(
            label="방문 횟수 csv파일 다운로드",
            data=sheet_data.to_csv(index=False).encode('cp949'),
            file_name='reserve_count.csv'
        )
    
def main():
    selected = option_menu(None,
        ["병원 클러스터링 결과 다운로드", "방문 횟수 조회"], 
        default_index=0, orientation="horizontal")

    menu_dict = {
        "병원 클러스터링 결과 다운로드" : {"fn": hos_info},
        "방문 횟수 조회" : {"fn": reserve_count},
    }

    if selected in menu_dict.keys():
        placeholder = st.empty()
        with placeholder.container():
            menu_dict[selected]["fn"]()

main()