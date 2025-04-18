import streamlit as st
import pandas as pd
from module.watcha_pedia_crawler import rankings_crawler
from module.watcha_pedia_crawler import comments_crawler
from datetime import datetime
import torch
from transformers import pipeline
import matplotlib.pyplot as plt


if "selected_movie_id" not in st.session_state:
    st.session_state['selected_movie_id'] = None


@st.cache_data(ttl=3600)
def get_rankings_data():
    rankings_crawler.crawl()
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    return [
        pd.read_csv("csv/box_office_ranking.csv"),
        pd.read_csv("csv/watcha_ranking.csv"),
        pd.read_csv("csv/netflix_ranking.csv"),
        update_time
    ]

@st.cache_data(ttl=3600)
def get_comments_data(movie_id):
    comments_crawler.crawl(movie_id)
    return pd.read_csv("csv/comments.csv")

def show_main():
    (
        box_office_ranking_df,
        watcha_ranking_df,
        netflix_ranking_df,
        update_time
    ) = get_rankings_data()

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
        div[class*=img-btn] {
            position: absolute;
            width: 100%;
            height: 100%;
        }
        div[class*=img-btn] > div {
            width: 100%;
            height: 100%;
        }
        div[class*=img-btn] > div > button {
            width: 100%;
            height: 100%;
            border: none;
            background-color: initial;
        }
        
        div[class*=back-btn] {
            position: absolute;
            width: 40px;
            height: 40px;
        }
        
        div[class*=back-btn] > button {
            width: 40px;
            height: 40px;
            border: none;
            background-color: initial;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('# 박스 오피스 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='box_office_ranking_update_button'):
        get_rankings_data.clear()
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
                if st.button("", key=f"{data['movie_id']}-img-btn"):
                    st.session_state['selected_movie_id'] = data['movie_id']  # 영화 데이터 저장
                    st.rerun()
    

    st.markdown('# 왓챠 영화 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='watcha_ranking_update_button'):
        get_rankings_data.clear()
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
                if st.button("", key=f"{data['movie_id']}-img-btn"):
                    st.session_state['selected_movie_id'] = data['movie_id']  # 영화 데이터 저장
                    st.rerun()

    st.markdown('# 넷플릭스 영화 순위 Top 10')
    if st.button(f"마지막 업데이트: {update_time} 🔄", key='netflix_ranking_update_button'):
        get_rankings_data.clear()
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
                if st.button("", key=f"{data['movie_id']}-img-btn"):
                    st.session_state['selected_movie_id'] = data['movie_id']  # 영화 데이터 저장
                    st.rerun()

def show_detail():
    st.markdown(
        """
        <style>
        div[class*=back-btn] {
            position: absolute;
            width: 32px;
            height: 32px;
        }
        
        div[class*=back-btn] > div {
            width: 100%;
            height: 100%;
        }
        div[class*=back-btn] > div > button {
            width: 100%;
            height: 100%;
            border: none;
            background-color: initial;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    comments_df = get_comments_data(st.session_state['selected_movie_id'])
    comments_df.info()
    comments_df['comment'] = comments_df['comment'].astype('string')
    comments_df.info()
    comments_df = comments_df[comments_df['comment'] != '']
    comments_df.info()
    comments_df = comments_df.dropna()
    comments_df.info()
    comments = comments_df['comment'].tolist()


    back_col = st.columns(1)[0]
    with back_col:
        st.markdown('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/></svg>', unsafe_allow_html=True)
        if st.button("", key="back-btn"):
            st.session_state.selected_movie_id = None
            st.rerun()

    st.markdown(f"# 영화 상세 정보")
    st.markdown(f"### 댓글 긍/부정 비율")
    st.dataframe(comments_df)

    classifier = pipeline(
        "sentiment-analysis",
        model="sangrimlee/bert-base-multilingual-cased-nsmc",
        tokenizer="sangrimlee/bert-base-multilingual-cased-nsmc"
    )

    # 감성분류 (batch로 여러 댓글 한 번에 예측)
    results = classifier(comments, truncation=True, max_length=128)
    # 결과에서 label만 추출
    pred_labels = [r['label'] for r in results]  # 'LABEL_0' (부정), 'LABEL_1' (긍정)

    # 원형 차트용 데이터 집계
    pos = pred_labels.count("positive")
    neg = pred_labels.count("negative")
    st.write(f"긍정: {pos}개, 부정: {neg}개")

    plt.rc('font', family='Malgun Gothic')
    plt.rc('axes', unicode_minus=False)
    fig, ax = plt.subplots()
    ax.pie([neg, pos], labels=["부정", "긍정"], autopct="%.1f%%", startangle=90, colors=['#ff9999','#66b3ff'])
    ax.axis('equal')
    st.pyplot(fig)

    # 각 항목별 결과 표로 보여주기
    # 결과 label을 한글로 변환
    label_map = {"negative": "부정", "positive": "긍정"}
    comments_df["분류결과"] = [label_map.get(l, l) for l in pred_labels]
    st.dataframe(comments_df[["comment", "분류결과"]])  # 필요한 열만 보여주기



def run_home():
    if st.session_state.selected_movie_id:
        show_detail()
    else:
        show_main()