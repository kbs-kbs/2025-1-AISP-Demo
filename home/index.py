import streamlit as st
import pandas as pd
from module.watcha_pedia_crawler import rankings_crawler
from module.watcha_pedia_crawler import comments_crawler
from datetime import datetime
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
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
                clicked = st.button("", key=f"{data['movie_id']}-img-btn")
                if clicked:
                    st.session_state['selected_movie_id'] = data['movie_id']  # 영화 데이터 저장
                    st.rerun()
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

def show_detail():
    comments_df = get_comments_data(st.session_state['selected_movie_id'])
    comments_df = comments_df.dropna(subset=['comment'])

    if st.button("← 목록으로 돌아가기"):
        st.session_state.selected_movie_id = None
        st.rerun()

    st.markdown(f"# 영화 상세 정보")
    st.markdown(f"## 댓글 긍/부정 비율")
    st.dataframe(comments_df)

    MODEL_NAME = "beomi/KcELECTRA-base"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()

    def batch_predict_sentiment(texts):
        inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            preds = torch.argmax(outputs.logits, dim=1).tolist()
        return preds

    comments = comments_df['comment'].astype(str).tolist()
    preds = []
    batch_size = 64
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i+batch_size]
        preds.extend(batch_predict_sentiment(batch))

    # ------------------------------
    # 여기서 부정/긍정 강제 뒤집기!!
    preds_named = []
    for p in preds:
        if p == 0:
            preds_named.append("긍정")
        elif p == 1:
            preds_named.append("부정")
    # ------------------------------

    pos = preds_named.count("긍정")
    neg = preds_named.count("부정")

    st.write(f"긍정: {pos}, 부정: {neg}")

    plt.rc('font', family='Malgun Gothic')
    plt.rc('axes', unicode_minus=False)
    fig, ax = plt.subplots()
    ax.pie([neg, pos], labels=["부정", "긍정"], autopct="%.1f%%", startangle=90, colors=['#ff9999','#66b3ff'])
    ax.axis('equal')
    st.pyplot(fig)



def run_home():
    if st.session_state.selected_movie_id:
        show_detail()
    else:
        show_main()