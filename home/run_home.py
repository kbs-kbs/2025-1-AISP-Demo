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

    st.markdown(
        """
        <style>
        .movie-rank {
            font-weight: bold;
        }

        .movie-title {
            font-weight: bold;
        }

        .field-name {
            margin-bottom: 0.25rem;
            font-size: 12px !important;
            color: gray;
        }

        .field-value {
            margin-bottom: 2rem;
        }
        
        .st-key-box_office_ranking_update_button > div > button {
            float: right;
            min-height: initial;
        }
        .st-key-box_office_ranking_update_button > div > button > div > p {
            font-size: 12px !important;
        }

        .st-key-watcha_ranking_update_button > div > button {
            float: right;
            min-height: initial;
        }
        .st-key-watcha_ranking_update_button > div > button > div > p {
            font-size: 12px !important;
        }

        .st-key-netflix_ranking_update_button > div > button {
            float: right;
            min-height: initial;
        }
        .st-key-netflix_ranking_update_button > div > button > div > p {
            font-size: 12px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('# 박스 오피스 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='box_office_ranking_update_button'):
        get_cached_data.clear()
        st.rerun()
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = box_office_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.markdown(
                    f'<p class="movie-rank">{data['rank']}위</p>', 
                    unsafe_allow_html=True
                )
                st.image(data['image_url'])
                st.markdown(
                    f'<p class="movie-title">{data["title"]}</p>', 
                    unsafe_allow_html=True
                )

                # 예매율/관객수 분할
                reservation, audience = st.columns(2)
                with reservation:
                    st.markdown(
                        '<p class="field-name">예매율</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['reservation']}</p>', 
                        unsafe_allow_html=True
                    )
                with audience:
                    st.markdown(
                        '<p class="field-name">관객 수</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['audience']}</p>', 
                        unsafe_allow_html=True
                    )
    

    st.markdown('# 왓챠 영화 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='watcha_ranking_update_button'):
        get_cached_data.clear()
        st.rerun()
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = watcha_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.markdown(
                    f'<p class="movie-rank">{data['rank']}위</p>', 
                    unsafe_allow_html=True
                )
                st.image(data['image_url'])
                st.markdown(
                    f'<p class="movie-title">{data["title"]}</p>', 
                    unsafe_allow_html=True
                )

                # 개봉년도/국가 분할
                release_year, country = st.columns(2)
                with release_year:
                    st.markdown(
                        '<p class="field-name">개봉 연도</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['release_year']}</p>', 
                        unsafe_allow_html=True
                    )
                with country:
                    st.markdown(
                        '<p class="field-name">국가</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['country']}</p>', 
                        unsafe_allow_html=True
                    )

    st.markdown('# 넷플릭스 영화 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='netflix_ranking_update_button'):
        get_cached_data.clear()
        st.rerun()
    for row in range(0, 10, 5):  # 0-4, 5-9
        cols = st.columns(5)
        for idx in range(5):
            data = netflix_ranking_df.iloc[row + idx]
            with cols[idx]:
                st.markdown(
                    f'<p class="movie-rank">{data['rank']}위</p>', 
                    unsafe_allow_html=True
                )
                st.image(data['image_url'])
                st.markdown(
                    f'<p class="movie-title">{data["title"]}</p>', 
                    unsafe_allow_html=True
                )

                # 개봉년도/국가 분할
                release_year, country = st.columns(2)
                with release_year:
                    st.markdown(
                        '<p class="field-name">개봉 연도</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['release_year']}</p>', 
                        unsafe_allow_html=True
                    )
                with country:
                    st.markdown(
                        '<p class="field-name">국가</p>', 
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<p class="field-value">{data['country']}</p>', 
                        unsafe_allow_html=True
                    )

    st.dataframe(box_office_ranking_df)
    st.dataframe(watcha_ranking_df)
    st.dataframe(netflix_ranking_df)