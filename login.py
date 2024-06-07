import streamlit as st
import pandas as pd
from clustering import Clustering

my_data = Clustering()

class Favorites:
    def __init__(self):
        self.favorites = pd.DataFrame(columns=['소재지도로명주소', '의료기관명', '연락처'])
    
    def add_favorites(self, hos):
        hos_name = hos['의료기관명']
        if hos_name not in self.favorites['의료기관명'].values:
            self.favorites = pd.concat([self.favorites, hos], ignore_index=True)
            st.write('즐겨찾기에 추가되었습니다.')
        else:
            st.write('이미 즐겨찾기에 추가된 병원입니다.')
        return
    
my_favorites = Favorites()

# 로그인 페이지
def login():
    st.title("로그인")
    username = st.text_input("사용자 이름", placeholder="medmil")
    password = st.text_input("비밀번호", type="password", placeholder="1234")
    login_button = st.button("로그인")

    if login_button:
        if username == "medmil" and password == "1234":
            st.success("로그인 성공!")
            st.session_state.role = "사용자"
            my_data.clustering()
        elif username == "admin" and password == "1234":
            st.success("로그인 성공!")
            st.session_state.role = "관리자"
            my_data.clustering()
        else:
            st.error("잘못된 사용자 이름 또는 비밀번호")
            st.session_state.role = None

