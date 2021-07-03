from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import random
import os
import SessionState

def get_session_state(rando):
    session_state = SessionState.get(random_number=random.random(), nsamples='')
    return session_state

def cacherando():
    rando = random_number=random.random()
    return rando

def display_app_header(main_txt,sub_txt,is_sidebar = False):
    html_temp = f"""
    <h1 style = "color:black; text_align:left;"> {main_txt} </h2>
    <h2 style = "color:black; text_align:left;"> {sub_txt} </p>
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
    rando = cacherando()
    session_state = get_session_state(rando)
    v_nsamples = int(os.getenv('V_NSAMPLES', 10)) # Number of competitors to generate
    sep = '<|endoftext|>'
    main_txt = """Calibre"""
    sub_txt = "Competitor Analysis"
    display_app_header(main_txt,sub_txt,is_sidebar = False)
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Configuration")
    session_state.nsamples = st.sidebar.slider("Number of Competitors to Analyse: ", 1, v_nsamples, 1)
    
    ### MAIN CONTENT ###
    session_state.domain = st.text_input("Your Website Domain: ", value='https://marymountwriters.com').lower()
    session_state.industry = st.text_input("Your Industry : ", value='Digital content marketing').lower()
    dataframe = np.random.randn(session_state.nsamples, 4)
    st.dataframe(dataframe)
       
if __name__ == "__main__":
    main()
