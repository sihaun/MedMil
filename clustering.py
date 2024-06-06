# 로그인 할 때 클러스터링 진행
import os
path = os.getcwd()

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans

hos_data_path = path + "/pages/Hospital.csv"

@st.cache_data
def load_hospital_data(hos_data_path):
    gangwon_hos = pd.read_csv(hos_data_path, encoding='cp949')
    return gangwon_hos

# 데이터 로드
gangwon_hos = load_hospital_data(hos_data_path)

class Clustering:
    __df = gangwon_hos

    __pub_health = __df[__df.의료기관종별.str.contains('보건|생활')].reset_index(drop=True)
    __dent = __df[__df.의료기관종별.str.contains('치과')].reset_index(drop=True)
    __normal_hos = __df[__df.의료기관종별.str.contains(r'^[병+의].*원$')].reset_index(drop=True)
    __oriental_hos = __df[__df.의료기관종별.str.contains(r'^한.*원$')].reset_index(drop=True)
    __mental_hos = __df[__df.의료기관종별.str.contains('정신')].reset_index(drop=True)
    __nursing_hos = __df[__df.의료기관종별.str.contains('요양')].reset_index(drop=True)
    __general_hos = __df[__df.의료기관종별.str.contains('종합병원')].reset_index(drop=True)
    __pharmacy = __df[__df.의료기관종별.str.contains('약국')].reset_index(drop=True)
    __plot_data = [__pub_health, __dent, __normal_hos, __oriental_hos, __mental_hos, __nursing_hos, __general_hos, __pharmacy]
    __k_hospital=[4, 5, 5, 5, 3, 3, 5, 5]

    def __init__(self):
        self.__centers = []

    def cluster_data(self, data, num_clusters):

        # 위도와 경도 데이터를 배열로 변환
        X = data[['경도', '위도']].values

        # KMeans 모델 생성 및 군집화 수행
        __kmeans = KMeans(n_clusters=num_clusters, random_state=0)
        data['cluster'] = __kmeans.fit_predict(X)

        # 각 클러슽터의 중심 위치를 반환
        __centers = __kmeans.cluster_centers_

        return data, __centers

    def clustering(self):
        for i, data in enumerate(self.__plot_data):
            self.__plot_data[i], center = self.cluster_data(data, self.__k_hospital[i])
            self.__centers.append(center)
        return 

    def get_clustered_data(self, index_hos):
        self.__df = self.__plot_data[index_hos][['소재지도로명주소', '의료기관명', '연락처', '거리(km)', '위도', '경도', 'cluster']]
        return self.__df
    
    def get_centers(self, index_hos):
        self.__df = self.__centers[index_hos]
        return self.__df

