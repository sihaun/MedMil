import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu

# 데이터 다운로드
gangwon_hos = pd.read_csv('https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000002797368&fileDetailSn=1&dataNm=%EA%B0%95%EC%9B%90%ED%8A%B9%EB%B3%84%EC%9E%90%EC%B9%98%EB%8F%84_%EC%9D%98%EB%A3%8C%EC%8B%9C%EC%84%A4%20%ED%98%84%ED%99%A9_20230821', encoding='cp949')

def search_hospital():

    st.session_state['selected_hos'] = None
    st.write("### 근처에 있는 병원 찾기")

    # Haversine 공식 함수
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # 지구 반지름 (단위: 킬로미터)
        lat1 = np.radians(lat1)
        lon1 = np.radians(lon1)
        lat2 = np.radians(lat2)
        lon2 = np.radians(lon2)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = R * c
        return distance

    # 자신의 위치를 가져와야 하나 일단은 임의로 지정.
    city = '국토정중앙천문대'
    latitude = 38.0688458
    longitude = 128.0298692

    gangwon_hos['거리(km)'] = haversine(latitude, longitude,
                                gangwon_hos.위도, gangwon_hos.경도).round(2)

    st.write('지금', city, "(", str(latitude), ", ", str(longitude), ") 에 있습니다.")

    # 전처리 과정
    pub_health = gangwon_hos[gangwon_hos.의료기관종별.str.contains('보건|생활')].reset_index(drop=True)
    dent = gangwon_hos[gangwon_hos.의료기관종별.str.contains('치과')].reset_index(drop=True)
    normal_hos = gangwon_hos[gangwon_hos.의료기관종별.str.contains(r'^[병+의].*원$')].reset_index(drop=True)
    oriental_hos = gangwon_hos[gangwon_hos.의료기관종별.str.contains(r'^한.*원$')].reset_index(drop=True)
    mental_hos = gangwon_hos[gangwon_hos.의료기관종별.str.contains('정신')].reset_index(drop=True)
    nursing_hos = gangwon_hos[gangwon_hos.의료기관종별.str.contains('요양')].reset_index(drop=True)
    general_hos = gangwon_hos[gangwon_hos.의료기관종별.str.contains('종합병원')].reset_index(drop=True)
    pharmacy = gangwon_hos[gangwon_hos.의료기관종별.str.contains('약국')].reset_index(drop=True)

    plot_data = [pub_health, dent, normal_hos, oriental_hos,
                mental_hos, nursing_hos, general_hos, pharmacy]
    plot_color = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige']
    plot_label = ['보건소계열', '치과', '일반병원', '한의원/한방병원', '정신병원', '요양병원', '종합병원', '약국']

    import folium
    from streamlit_folium import st_folium

    with st.form("near_hos_form"):
        find_radius = st.select_slider(
            "찾을 범위(km)을 설정해 주십시오.",
            options=[x for x in range(101)])
        hospital = st.radio(
                        "찾고자 하는 의료기관을 선택하십시오.",
                        plot_label,
                        horizontal=True
                    )
        st.write("반경 " + str(find_radius) + "km 내에서 "
                 + hospital + " 탐색")
        st.form_submit_button('탐색하기')

    plot_map = folium.Map(location=[latitude, longitude], zoom_start=9)

    folium.Marker([latitude, longitude], icon=folium.Icon(color = 'cadetblue'), popup=folium.Popup(city, max_width=300)).add_to(plot_map)

    folium.Circle(
        location=[latitude, longitude],
        radius=find_radius * 1000,
        color="#eb9e34",
        fill_color="red"
    ).add_to(plot_map)

    from st_aggrid import AgGrid, GridOptionsBuilder

    for i, data in enumerate(plot_data):
        if plot_label[i] == hospital:
            sheet_data = plot_data[i][['소재지도로명주소', '의료기관명', '연락처', '거리(km)', '위도', '경도']]
            sheet_data = sheet_data[sheet_data['거리(km)'] <= find_radius].reset_index(drop=True)
            for j in range(len(sheet_data)):
                location = [sheet_data.위도[j], sheet_data.경도[j]]
                folium.Marker(location, icon=folium.Icon(color = plot_color[i]),
                            popup=folium.Popup(sheet_data.의료기관명[j], max_width=300)).add_to(plot_map)

    st_data = st_folium(plot_map, height=500, width=500)

    sheet_data = sheet_data[['소재지도로명주소', '의료기관명', '연락처', '거리(km)']].sort_values('거리(km)')

    gd = GridOptionsBuilder.from_dataframe(sheet_data)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(sheet_data, height=300, gridOptions=gridoptions, fit_columns_on_grid_load=True)

    import urllib.parse

    # 네이버 지도 연결
    try:
        selected_hos = grid_table.selected_rows[0]
        url_name = selected_hos['소재지도로명주소']
        st.write('### ' + selected_hos['의료기관명'])
        st.write(url_name)
        encoded_text_mobile = urllib.parse.quote(url_name)
        encoded_text_pc = url_name.replace(' ', '+')
        st.session_state['selected_hos'] = selected_hos

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.link_button("네이버 지도로 확인하기(모바일)",
                        "nmap://search?query=" + encoded_text_mobile + "&appname=com.example.myapp")
        with col2:
            st.link_button("네이버에서 확인하기(PC)",
                        "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=" + encoded_text_pc)
        with col3:                
            st.button("예약하기")

    except:
        pass

def reserve():

    st.write("### 예약하기")
    with st.form("hos_name_form"):

        try:
            selected_value = st.session_state.selected_hos['의료기관명']
            st.write('병원 찾기에서 선택한 병원으로 자동 채우기 되었습니다.')
        except:
            selected_value = ''

        hos_name = st.text_input("병원명", selected_value,
                                 placeholder='병원명을 입력하세요.')

        import datetime
        col1, col2 = st.columns(2)

        with col1:
            d = st.date_input("예약 날짜")
            
        with col2:
            t = st.time_input('예약 시간', None, step=1800)

        st.form_submit_button('예약하기')

    if (hos_name != '') & (t != None):
        try:
            st.write(f'예약한 병원: {hos_name}')
            st.write(f'예약 날짜 및 시간: {d}, {t.hour}시 {t.minute}분')
        except:
            pass

    else:
        st.write('내용을 확인해 주세요.')

def favorites():
    st.write("### 즐겨찾기")

def main():
    selected = option_menu(None,
        ["병원 찾기", "예약하기", "즐겨찾기"], 
        icons=['geo-alt', 'clock', 'star'],
        menu_icon="cast",
        default_index=0, orientation="horizontal")

    menu_dict = {
        "병원 찾기" : {"fn": search_hospital},
        "예약하기" : {"fn": reserve},
        "즐겨찾기" : {"fn": favorites}
    }

    if selected in menu_dict.keys():
        placeholder = st.empty()
        with placeholder.container():
            menu_dict[selected]["fn"]()

main()
