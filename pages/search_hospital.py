import os
path = os.getcwd()

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from st_aggrid import AgGrid, GridOptionsBuilder
from menu import menu_with_redirect
from login import my_data

menu_with_redirect()

# 병원 데이터 다운로드
army_data_path = path + "/pages/Army_Unit.csv"
hos_data_path = path + "/pages/Hospital.csv"
@st.cache_data
def load_hospital_data(hos_data_path):
    gangwon_hos = pd.read_csv(hos_data_path, encoding='cp949')
    return gangwon_hos
@st.cache_data
def load_army_data(army_data_path):
    army_data = pd.read_csv(army_data_path, encoding='cp949')
    return army_data

def matching(centers, army_path, index):
    # 병원 군집화 데이터
    hospital_centers = centers

    # 군부대 데이터 로드
    army = load_army_data(army_path)
    army_locations = army[['경도', '위도']].values[[index]]

    # 군부대와 병원 군집 중심 좌표 매칭
    distances = np.zeros((army_locations.shape[0], hospital_centers.shape[0]))

    for i in range(army_locations.shape[0]):
        for j in range(hospital_centers.shape[0]):
            distances[i, j] = np.linalg.norm(army_locations[i] - hospital_centers[j])

    # 매칭 결과
    matched_centers = np.argmin(distances, axis=1)[0]
    print(matched_centers)
    
    # 선택한 군부대와 가장 가까운 병원 군집 중심 좌표 반환
    closest_hospital_centers = hospital_centers[matched_centers]
    
    return closest_hospital_centers, matched_centers

# Haversine 공식 함수 정의
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


# 데이터 로드
gangwon_hos = load_hospital_data(hos_data_path)
army_data = load_army_data(army_data_path)
k_hospital=[4, 5, 5, 5, 3, 3, 5, 5] # 각 병원 종류별 클러스터 수

# 사용자에게 병원 찾기 메시지 표시
st.write("### 병원 검색")

army_label = army_data['보병사단'] # 군부대 이름 리스트

def search_hospital():
    # 현 군부대 위치 선택
    with st.form("select_army"):
        army = st.radio("현재 위치한 군부대를 선택하십시오.", army_label, horizontal=True)
        st.write(army, "을(를) 선택하셨습니다.")
        index_army = army_label.tolist().index(army)  # 현재 위치한 군부대의 인덱스

        st.form_submit_button('선택하기')

    # 사용자의 위치 설정 (현 군부대로 지정)
    city = army
    latitude = army_data.loc[army_data['보병사단'] == army, '위도'].values[0]
    longitude = army_data.loc[army_data['보병사단'] == army, '경도'].values[0]

    # 각 병원과 사용자의 위치 사이의 거리 계산
    gangwon_hos['거리(km)'] = haversine(latitude, longitude, gangwon_hos.위도, gangwon_hos.경도).round(2)

    # 결과를 CSV 파일에 추가
    gangwon_hos.to_csv(path + '/pages/Hospital.csv', index=False, encoding='cp949')

    # 병원 종류 선택
    plot_label = ['보건소계열', '치과', '일반병원', '한의원/한방병원', '정신병원', '요양병원', '종합병원', '약국']

    # 사용자에게 입력 받기 위한 폼 생성
    with st.form("select_hospital"):
        #find_radius = st.select_slider("찾을 범위(km)을 설정해 주십시오.", options=[x for x in range(101)])
        #st.write("반경 " + str(find_radius) + "km 내에서 탐색")
        hospital = st.radio("찾고자 하는 의료기관을 선택하십시오.", plot_label, horizontal=True)
        st.write(hospital, "을(를) 선택하셨습니다.")
        index_hos = plot_label.index(hospital) # 선택한 병원의 인덱스
        const_k = k_hospital[index_hos] # 선택한 병원의 클러스터 수
        st.form_submit_button('탐색하기')

    plot_color = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige']

    # 선택한 병원에 대한 클러스터링 결과 가져오기
    df = my_data.get_clustered_data(index_hos)
    # get_clustered_data 메서드 호출
    centers = my_data.get_centers(index_hos)

    # 병원과 군부대 매칭 후 선택한 군부대와 가장 가까운 마을 중심과 인덱스 가져오기
    closest_town, index_town = matching(centers, army_data_path, index_army)

    matched_cluster = df[df['cluster'] == index_town]

    # 매칭된 클러스터에 해당하는 병원 데이터 가져오기

    # 지도 생성
    plot_map = folium.Map(location=[latitude, longitude], zoom_start=9)

    # 사용자의 위치를 지도에 표시
    folium.Marker([latitude, longitude], icon=folium.Icon(color = 'cadetblue'), popup=folium.Popup(city, max_width=300)).add_to(plot_map)

    find_radius = 1557
    # 사용자의 위치를 중심으로 한 원을 그려 탐색 범위를 표시
    #folium.Circle(location=[latitude, longitude], radius=find_radius * 1000, color="#eb9e34", fill_color="red").add_to(plot_map)

    # 매칭된 병원 데이터를 지도에 표시
    sheet_data = matched_cluster[['소재지도로명주소', '의료기관명', '연락처', '거리(km)', '위도', '경도']]
    sheet_data = sheet_data[sheet_data['거리(km)'] <= find_radius].reset_index(drop=True)
    for j in range(len(sheet_data)):
                location = [sheet_data.위도[j], sheet_data.경도[j]]
                folium.Marker(location, icon=folium.Icon(color = plot_color[index_hos]), popup=folium.Popup(sheet_data.의료기관명[j], max_width=300)).add_to(plot_map)


    # 사용자의 현재 위치 표시
    st.write('지금', city, "(", str(latitude), ", ", str(longitude), ") 에 있습니다.")
    # 지도를 Streamlit에서 표시
    st_data = st_folium(plot_map, height=500, width=700)

    # 병원의 정보를 거리순으로 정렬
    sheet_data = sheet_data[['소재지도로명주소', '의료기관명', '연락처', '거리(km)']].sort_values('거리(km)')
    # AgGrid를 사용하여 병원의 정보를 표 형태로 표시
    gd = GridOptionsBuilder.from_dataframe(sheet_data)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(sheet_data, height=300, gridOptions=gridoptions, fit_columns_on_grid_load=True)

    import urllib.parse

    try:
        # 네이버 지도 연결
        selected_hos = grid_table.selected_data
        url_name = selected_hos['소재지도로명주소'][0]
        st.write('### ' + selected_hos['의료기관명'][0])
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
            st.page_link('pages/reserve.py', label="예약하기")
    
    except:
        pass


search_hospital()