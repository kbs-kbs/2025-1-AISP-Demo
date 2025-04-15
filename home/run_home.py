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
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = box_office_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.write(data.ranking)
                st.image(data.image_url)
                st.write(data.title)

                # 개봉년도/국가 분할
                release_year, country = st.columns(2)
                release_year.write(str(data.release_year))
                country.write(data.country)

                # 예매율/관객수 분할
                reservation, audience = st.columns(2)
                reservation.write(data.reservation)
                audience.write(data.audience)
    

    st.markdown('# 왓챠 영화 순위 Top 10')
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = watcha_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.write(data.ranking)
                st.image(data.image_url)
                st.write(data.title)

                # 개봉년도/국가 분할
                release_year, country = st.columns(2)
                release_year.write(str(data.release_year))
                country.write(data.country)

    st.markdown('# 넷플릭스 영화 순위 Top 10')
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = netflix_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.write(data.ranking)
                st.image(data.image_url)
                st.write(data.title)

                # 개봉년도/국가 분할
                release_year, country = st.columns(2)
                release_year.write(str(data.release_year))
                country.write(data.country)


    st.dataframe(box_office_ranking_df)
    st.dataframe(watcha_ranking_df)
    st.dataframe(netflix_ranking_df)