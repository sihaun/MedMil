import streamlit as st
from clustering import Clustering

my_data = Clustering()

# 로그인 페이지
def login():
    st.title("로그인")
    username = st.text_input("사용자 이름", placeholder="medmil")
    password = st.text_input("비밀번호", type="password",
                             placeholder="1234")
    login_button = st.button("로그인")

    if login_button:
        if username == "medmil" and password == "1234":
            st.success("로그인 성공!")
            st.session_state.role = "사용자"
            my_data.clustering()
        else:
            st.error("잘못된 사용자 이름 또는 비밀번호")
            st.session_state.role = None

