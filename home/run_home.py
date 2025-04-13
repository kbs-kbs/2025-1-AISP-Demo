import streamlit as st
from module.watcha_pedia_scraper.run_ranking_scraper import run_ranking_scraper

# @st.cache_data(ttl=3600)
def get_cached_data():
    return run_ranking_scraper()

def run_home():
    ranking_df = get_cached_data()  # 캐시된 데이터 사용

    st.markdown('# 박스 오피스 순위 Top 10')
    st.dataframe(ranking_df)