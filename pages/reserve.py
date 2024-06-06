import streamlit as st
from menu import menu_with_redirect
menu_with_redirect()
def reserve():

    st.write("### 예약하기")
    with st.form("hos_name_form"):

        try:
            selected_value = st.session_state.selected_hos['의료기관명'][0]
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

reserve()