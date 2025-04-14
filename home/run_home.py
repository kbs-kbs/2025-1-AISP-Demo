import streamlit as st
import pandas as pd
import module.watcha_pedia_crawler.rankings_crawler as wc

# @st.cache_data(ttl=3600)
def get_cached_data():
    wc.crawl()
    return [
        pd.read_csv("csv/box_office_ranking.csv"),
        pd.read_csv("csv/watcha_ranking.csv"),
        pd.read_csv("csv/netflix_ranking.csv")
    ]

def run_home():
    (
        box_office_ranking_df,
        watcha_ranking_df,
        netflix_ranking_df
    ) = get_cached_data()

    st.markdown('# 박스 오피스 순위 Top 10')
    st.dataframe(box_office_ranking_df)

    st.markdown('# 왓챠 영화 순위 Top 10')
    st.dataframe(watcha_ranking_df)

    st.markdown('# 넷플릭스 영화 순위 Top 10')
    st.dataframe(netflix_ranking_df)