import streamlit as st
from menu import menu_with_redirect
from advertise import advertise
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from login import my_favorites
from pages.search_hospital import load_hospital_data
menu_with_redirect()
advertise()
        
hos_data = load_hospital_data('pages/Hospital.csv')
hos_data = hos_data[['소재지도로명주소', '의료기관명', '연락처']]
def favorites():
    st.write("### 즐겨찾기")
    with st.form("hos_name_form"):

        try:
            hos_name = st.session_state.selected_hos['의료기관명'][0]

        except:
            hos_name = 'hi'

        hos_name = st.text_input("병원명", hos_name,
                                 placeholder='병원명을 입력하세요.')

        if st.form_submit_button('추가하기'):
            hos = hos_data[hos_data['의료기관명'] == hos_name]
            my_favorites.add_favorites(hos)

    data = my_favorites.favorites[['소재지도로명주소', '의료기관명', '연락처']].sort_values('의료기관명', ascending=False).reset_index(drop=True)
    # AgGrid를 사용하여 병원의 정보를 표 형태로 표시
    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(data, height=800, gridOptions=gridoptions, fit_columns_on_grid_load=True)
    selected_hos = grid_table.selected_data
    st.session_state['selected_hos'] = selected_hos
    st.page_link('pages/reserve.py', label="예약하기")

favorites()