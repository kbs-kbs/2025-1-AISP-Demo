import streamlit as st
from streamlit_option_menu import option_menu
from home.index import run_home

if "selected_movie_id" not in st.session_state:
    st.session_state['selected_movie_id'] = None

def main():
    st.set_page_config(page_title="캡슐러", layout='wide')
    st.markdown("""
    <style>
    #stDecoration {
        display: none;
    }
    .stAppHeader {
        height: 4.25rem;
    }
    #root > div:nth-of-type(1) > div.withScreencast > div > div > section > div.stMainBlockContainer > div > div > div > div:nth-of-type(1) {
        display: none;
    }
    #root > div:nth-of-type(1) > div.withScreencast > div > div > section > div.stMainBlockContainer > div > div > div > div:nth-of-type(2) {
        position: fixed;
        top: 1.25rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999990;
    }
    [data-testid="stCustomComponentV1"] {
        width: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    st.logo("images/logo-default.svg", size="large")
    selected = option_menu(
        None, ["홈", "북마크"],
        icons=[" ", " "],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": 0,
                "background-color": "unset",
                "border-radius": "unset",
            },
            "nav-link-selected": {
                "margin": "0",
                "padding": "0.25rem",
                "background-color": "unset",
                "border-radius": "unset",
                "font-size": "0.875rem",
                "font-weight": "bold",
                "color": "var(--primary-color)"
            },
            "nav-link": {
                "margin": "0",
                "padding": "0.25rem",
                "font-size": "0.875rem",
                "font-weight": "bold",
                "color": "gray"
            },
        }
    )
    if selected == "홈":
        run_home()
    elif selected == "북마크":
        pass
    else:
        print("error..")
        
if __name__ == "__main__":
    main()