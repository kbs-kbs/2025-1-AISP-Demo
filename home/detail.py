import streamlit as st
import pandas as pd
import module.watcha_pedia_crawler.rankings_crawler as wc
from datetime import datetime

@st.cache_data(ttl=3600)
def get_cached_data():
    wc.crawl()
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    return [
        pd.read_csv("csv/box_office_ranking.csv"),
        pd.read_csv("csv/watcha_ranking.csv"),
        pd.read_csv("csv/netflix_ranking.csv"),
        update_time
    ]

def run_home():
    (
        box_office_ranking_df,
        watcha_ranking_df,
        netflix_ranking_df,
        update_time
    ) = get_cached_data()