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
    
def generate_competitors(domain,industry,nsamples):
    col = ['Competitor','Similarity','Channels','Target Keywords']
    competitors = ['Union Square','Chernobyl Industries','Neverland','Crocodile Inc.','Yellow Tail','Lorem Ipsum','Elid.Net','Hannibal L.','Teriyaki','BKT Holdings']
    channels = ['Facebook','Instagram','Twitter','LinkedIn','Blog','MailChimp','Weibo']
    keywords = ['Content Marketing','Copywriting','SEO','SEM','Marketing ROI','Marketing Agency']
    dataframe = pd.DataFrame(list(zip(competitors[:nsamples],
                                      np.random.randn(nsamples),
                                      [np.random.choice(channels,3) for i in range(nsamples)],
                                      [np.random.choice(keywords,3) for i in range(nsamples)])),
                             columns=col)
    return dataframe

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
    if st.button('Generate Competitor Analysis'):
        session_state.generated = generate_competitors(session_state.domain,session_state.industry,session_state.nsamples)
        st.header('Your competitor(s):')
        st.dataframe(session_state.generated)
       
if __name__ == "__main__":
    main()
