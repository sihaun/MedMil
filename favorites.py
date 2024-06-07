import pandas as pd
import streamlit as st

hos_data_path = "pages/Hospital.csv"
hos_data = pd.read_csv(hos_data_path, encoding='cp949')

class Favorites:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Favorites, cls).__new__(cls, *args, **kwargs)
        return cls._instance  

    def __init__(self):
        self.favorites = pd.DataFrame(columns=['소재지도로명주소', '의료기관명', '연락처'])
        self.hos_data = hos_data[['소재지도로명주소', '의료기관명', '연락처']]
    
    def add_favorites(self, hos_name):
        if hos_name in self.favorites['의료기관명'].values:
            st.write('이미 추가된 병원입니다.')
            return
        
        selected_hos = self.hos_data[self.hos_data['의료기관명'] == hos_name]
        self.favorites = pd.concat([self.favorites, selected_hos])
        st.session_state['selected_hos'] = selected_hos
        st.write(f'{hos_name}을(를) 즐겨찾기에 추가했습니다.')
    
