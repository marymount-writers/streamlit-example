from collections import namedtuple
import altair as alt
import math
import pandas as pd
import numpy as np
import streamlit as st
import random
import time
import os
import SessionState

def get_session_state(rando):
    session_state = SessionState.get(random_number=random.random(), nsamples='', 
                                     generated=pd.DataFrame(columns=['Competitor','Similarity','Channels','Target Keywords']))
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
                                      [', '.join(np.random.choice(channels,3,replace=False)) for i in range(nsamples)],
                                      [', '.join(np.random.choice(keywords,3,replace=False)) for i in range(nsamples)])),
                             columns=col)
    return dataframe

def main():
    st.set_page_config(page_title='📝 Calibre',layout='wide')
    rando = cacherando()
    session_state = get_session_state(rando)
    v_nsamples = int(os.getenv('V_NSAMPLES', 10)) # Number of competitors to generate
    sep = '<|endoftext|>'
    main_txt = """📝 Calibre"""
    awareness_stages = ['Unaware of solution','Aware of solution','Interested in product offered',
                        'Considering purchase','Intending to purchase','Existing product user']
    fin_comps = ['Fire Finance','Wallet Philosophy','Vision Advisory']
    df_tsne = pd.read_csv('data/fin_tsne.csv',index_col=0)
    df_tsne.competitor = [fin_comps[i] for i in df_tsne.competitor]
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Menu")
    session_state.pages = st.sidebar.radio("Navigate Calibre", options=['Competitor Profile','Semantic Fingerprinting','Sentiment Heatmapping'])
    display_side_panel_header("Configuration")
    session_state.nsamples = st.sidebar.slider("Number of Competitors to Analyse: ", 1, v_nsamples, 1)
    display_side_panel_header("Audience Profile")
    session_state.audience_age = st.sidebar.slider("Audience Age Range: ", 16, 65, (26, 30))
    session_state.audience_awareness = st.sidebar.selectbox("Audience Awareness: ", options=awareness_stages)
    
    ### COMPETITOR PROFILE ###
    if session_state.pages == 'Competitor Profile':
        sub_txt = "Competitor Profile"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        session_state.domain = st.text_input("Your Website Domain: ", value='https://marymountwriters.com').lower()
        session_state.industry = st.text_input("Your Industry : ", value='Digital content marketing').lower()

        session_state.generated = generate_competitors(session_state.domain,session_state.industry,session_state.nsamples)
        st.header('Your competitors:')
        st.dataframe(session_state.generated,use_container_width=True)
    
    ### GENERATE COMPETITORS ###
    if session_state.pages == 'Semantic Fingerprinting':
        sub_txt = "Semantic Fingerprinting"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        compSelect = st.multiselect('Select competitors to view:',options=fin_comps)
        c = alt.Chart(df_tsne, height=600).mark_circle(size=10).encode(x='Dim1', y='Dim2',
                                                                color='competitor', 
                                                                tooltip=['competitor','tokens']).transform_filter(
            alt.FieldOneOfPredicate(field='competitor', oneOf=compSelect))
            
        st.altair_chart(c, use_container_width=True)
                    
    ### GENERATE CONTENT BRIEF ###
#     if session_state.pages == 'Topical Matrix Analysis':
#         sub_txt = "Topical Matrix Analysis"
#         display_app_header(main_txt,sub_txt,is_sidebar = False)        
        
    ### SENTIMENT HEATMAPPING ###
    if session_state.pages == 'Sentiment Heatmapping':
        sub_txt = "Sentiment Heatmapping"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        
if __name__ == "__main__":
    main()
