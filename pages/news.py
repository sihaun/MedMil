import streamlit as st
import streamlit_shadcn_ui as ui
from local_components import card_container
import pandas as pd
from menu import menu_with_redirect
from advertise import advertise

menu_with_redirect()
advertise()

st.markdown('''
<style>
.st-emotion-cache-vdokb0 p {
    color: #1a202c;
    margin: 2px;
}
</style>
''', unsafe_allow_html=True)

st.write("### 건강 정보")

infection = pd.read_csv('pages/Infection.csv', encoding='cp949')
option_list = list(set(infection.연도))
option_list.sort()

st.write('#### 연도별 질병 현황')

col1, col2 = st.columns(2)
with col1:
    
    st.write('조회연도')
    selected_year = ui.tabs(options=option_list[-4:],
                            default_value=option_list[-1],
                            key="select_year")
with col2:
    st.write('조회분기')
    selected_quarter = ui.tabs(options=['1분기', '2분기', '3분기', '4분기'],
                               default_value='1분기',
                               key="select_quarter")
    selected_quarter = int(selected_quarter[:1])

with card_container(key="chart"):
    select_data = infection[infection.연도 == selected_year]
    select_data = select_data[select_data.분기구분 == selected_quarter]
    plot_data = select_data.groupby('질병명').sum('현황')['현황']
    st.bar_chart(plot_data, use_container_width=True)
    
show_text = str(plot_data.index[plot_data.argmax()])
if len(show_text) <= 3:
    show_text = show_text.replace(' ', '')

from bs4 import BeautifulSoup
import requests

url = f'https://terms.naver.com/search.naver?query={show_text}&searchType=&dicType=&subject='
html = BeautifulSoup(requests.get(url, headers={'User-agent':'Mozilla/5.0'}).text, 'lxml')
pgrr = html.find('ul', class_='content_list')
go_to = 'https://terms.naver.com' + pgrr.a['href']

col3, col4 = st.columns(2)

with col3:
    with ui.card():
        ui.element('h1', children=['조심해야 할 전염병'], className="text-gray-500 text-sm font-medium m-1",
                   key="label1")
        ui.element('h2', children=[show_text], className="text-gray-900 text-3xl font-bold m-1",
                   key="label2")
        ui.element('link_button', text='자세히 알아보기', url=go_to)

with col4:
    with card_container(key='sheet'):
        plot_table = select_data.sort_values(by='현황', ascending=False).head(5)[['질병명', '현황']]
        ui.table(plot_table)
