import streamlit as st
from menu import menu
from login import login

# st.session_state.role을 None으로 초기화
if "role" not in st.session_state:
    st.session_state.role = None

# 위젯을 초기화하기 위해 세션 상태에서 역할을 가져옴
st.session_state._role = st.session_state.role

# 로그인 페이지 실행
login()

menu() # 메뉴 표시