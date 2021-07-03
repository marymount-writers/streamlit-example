from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import os
import SessionState

def get_session_state(rando):
    session_state = SessionState.get(random_number=random.random(), nsamples='')
    return session_state

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    html_temp = f"""
    <h2 style = "color:black; text_align:center;"> {main_txt} </h2>
    <p style = "color:black; text_align:center;"> {sub_txt} </p>
    </div>
    """
    if is_sidebar:
        st.sidebar.markdown(html_temp, unsafe_allow_html = True)
    else: 
        st.markdown(html_temp, unsafe_allow_html = True)
        
def display_side_panel_header(txt):
    st.sidebar.markdown(f'## {txt}')

def main():
    st.set_page_config(page_title='Calibre') #layout='wide', initial_sidebar_state='auto'
    session_state = get_session_state(rando)
    v_nsamples = int(os.getenv('V_NSAMPLES', 10)) # Number of competitors to generate
    sep = '<|endoftext|>'
    main_txt = """Calibre"""
    sub_txt = "Competitor Analysis"
    display_app_header(main_txt,sub_txt,is_sidebar = False)
    session_state.domain = st.text_input("Your Website Domain: ", value='').lower()
    
    display_side_panel_header("Configuration")
    session_state.nsamples = st.sidebar.slider("Number of Competitors to Analyse: ", 1, v_nsamples, 1)
    
if __name__ == "__main__":
    main()
