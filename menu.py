import streamlit as st
import os
path = os.getcwd()
def authenticated_menu():
    # 인증된 사용자를 위한 링크 표시
    #st.sidebar.page_link("info.py", label="계정 정보") # 사용자 정보 페이지로 이동
    st.sidebar.page_link("pages\\news.py", label="건강 정보") # 사용자 정보 페이지로 이동
    st.sidebar.page_link("pages\\search_hospital.py", label="병원 검색") # 메인 페이지로 이동
    st.sidebar.page_link("pages\\reserve.py", label="예약하기") # 예약 페이지로 이동
    st.sidebar.page_link("pages\\bookmark.py", label="즐겨찾기") # 즐겨찾기 페이지로 이동
    
    # 관리자 및 슈퍼 관리자 역할에 대한 추가 링크 표시
    if st.session_state.role in ["관리자"]:
        st.sidebar.page_link("pages\\admin.py", label="관리자 페이지") # 즐겨찾기 페이지로 이동
    

def unauthenticated_menu():
    # 인증되지 않은 사용자를 위한 링크 표시
    st.sidebar.page_link("app.py", label="로그인")


def menu():
    # 사용자가 인증되었는지 확인
    if "role" not in st.session_state or st.session_state.role is None:
        # 인증되지 않은 메뉴 표시
        unauthenticated_menu()
        return
    
    # 인증된 메뉴 표시
    authenticated_menu()


def menu_with_redirect():
    # 사용자가 인증되었는지 확인
    if "role" not in st.session_state or st.session_state.role is None:
        # 로그인 페이지로 리디렉션
        st.switch_page("app.py")
    
    # 메뉴 표시
    menu()
