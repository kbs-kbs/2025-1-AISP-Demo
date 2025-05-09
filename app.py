import streamlit as st
from streamlit_option_menu import option_menu
from home.index import run_home

if "selected_movie_id" not in st.session_state:
    st.session_state['selected_movie_id'] = None

def main():
    st.set_page_config(page_title="캡슐러", layout='wide')
    with st.sidebar:
        selected = option_menu(
            "메뉴", ["홈", "북마크"],
            icons=["house", "bookmark"],
            menu_icon="list", default_index=0
        )
        
    if selected == "홈":
        run_home()
    elif selected == "북마크":
        pass
    else:
        print("error..")
        
if __name__ == "__main__":
    main()