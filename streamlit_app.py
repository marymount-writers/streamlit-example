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
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download(["stopwords","vader_lexicon"])
stopwords = nltk.corpus.stopwords.words("english")

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
    competitors = ['Freia Medical','Halley Medical Aesthetics','Self Medical Aesthetics','The Aesthetics Centre','The Clifford Strategy',
                  'Dr David Aesthetics','PLA Medical','Botox Centre','Singapore Clinic of Aesthetics','Plastic Hub']
    channels = ['Facebook','Instagram','Twitter','LinkedIn','Blog','MailChimp','Weibo']
    keywords = ['Treatment','Botox','Injectables','Aesthetic','Clinic','Risks','Safety','Tolerance','Skincare','Hair','Facial','Mask','Acne']
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
    aes_comps = ['Freia Medical','Halley Medical Aesthetics','Self Medical Aesthetics','The Aesthetics Centre','The Clifford Strategy']
    fin_tsne = pd.read_csv('data/fin_tsne.csv',index_col=0)
    fin_tsne.competitor = [fin_comps[i] for i in fin_tsne.competitor]
    aes_tsne = pd.read_csv('data/aes_tsne.csv',index_col=0)
    aes_tsne.competitor = [aes_comps[i] for i in aes_tsne.competitor]
    fin_words = pd.read_csv('data/fin_words.csv',index_col=0)
    aes_words = pd.read_csv('data/aes_words.csv',index_col=0)
    
    ### SIDEBAR CONTENT ###
    display_side_panel_header("Menu")
    session_state.pages = st.sidebar.radio("Navigate Calibre", options=['Competitor Profile','Semantic Fingerprinting','Sentiment Heatmapping'])
    display_side_panel_header("Configuration")
    session_state.nsamples = st.sidebar.slider("Number of Competitors to Analyse: ", 1, v_nsamples, 1)
    display_side_panel_header("Audience Profile")
    session_state.audience_age = st.sidebar.slider("Audience Age Range: ", 16, 65, (26, 30))
    session_state.audience_awareness = st.sidebar.selectbox("Audience Awareness: ", options=awareness_stages)
    display_side_panel_header("Industry")
    session_state.ind_type = st.sidebar.radio("Select Industry", options=['Finance','Aesthetics'])
    if session_state.ind_type == 'Finance':
        df_tsne = fin_tsne
        df_comps = fin_comps
        df_words = fin_words
    else:
        df_tsne = aes_tsne
        df_comps = aes_comps
        df_words = aes_words
    
    ### COMPETITOR PROFILE ###
    if session_state.pages == 'Competitor Profile':
        sub_txt = "Competitor Profile"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        session_state.domain = st.text_input("Your Website Domain: ", value='https://marymountwriters.com').lower()
        session_state.industry = st.text_input("Your Industry : ", value='Digital content marketing').lower()

        session_state.generated = generate_competitors(session_state.domain,session_state.industry,session_state.nsamples)
        st.header('Your competitors:')
        st.dataframe(session_state.generated)
    
    ### GENERATE COMPETITORS ###
    if session_state.pages == 'Semantic Fingerprinting':
        sub_txt = "Semantic Fingerprinting"
        display_app_header(main_txt,sub_txt,is_sidebar = False)
        
        compSelect = st.multiselect('Select competitors to view:',options=df_comps,default=df_comps)
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
                
        sia = SentimentIntensityAnalyzer()
        pos = []
        neg = []
        neu = []
        for i, article in enumerate(df_words.text):
          pos.append(sia.polarity_scores(article)['pos'])
          neg.append(sia.polarity_scores(article)['neg'])
          neu.append(sia.polarity_scores(article)['neu'])
        
        avg_pos = []
        avg_neg = []
        avg_neu = []
        range_pos = []
        range_neg = []
        range_neu = []
        if session_state.ind_type == 'Finance':
            comp_range = [0,5,12,22]
        else:
            comp_range = [0,25,50,58,83,108]

        for i in range(len(df_comps)):
          avg_pos.append(np.average(pos[comp_range[i]:comp_range[i+1]]))
          range_pos.append(np.max(pos[comp_range[i]:comp_range[i+1]])-np.min(pos[comp_range[i]:comp_range[i+1]]))
          avg_neg.append(np.average(neg[comp_range[i]:comp_range[i+1]]))
          range_neg.append(np.max(neg[comp_range[i]:comp_range[i+1]])-np.min(neg[comp_range[i]:comp_range[i+1]]))
          avg_neu.append(np.average(neu[comp_range[i]:comp_range[i+1]]))
          range_neu.append(np.max(neu[comp_range[i]:comp_range[i+1]])-np.min(neu[comp_range[i]:comp_range[i+1]]))
        
        avg_s = pd.DataFrame(columns=['Score','Sentiment','Competitor'])
        avg_s = avg_s.append(pd.DataFrame(zip(avg_pos,['Positive']*len(df_comps),df_comps),columns=['Score','Sentiment','Competitor']))
        avg_s = avg_s.append(pd.DataFrame(zip(avg_neg,['Negative']*len(df_comps),df_comps),columns=['Score','Sentiment','Competitor']))

        range_s = pd.DataFrame(columns=['Score','Sentiment','Competitor'])
        range_s = range_s.append(pd.DataFrame(zip(range_pos,['Positive']*len(df_comps),df_comps),columns=['Score','Sentiment','Competitor']))
        range_s = range_s.append(pd.DataFrame(zip(range_neg,['Negative']*len(df_comps),df_comps),columns=['Score','Sentiment','Competitor']))
        
        avg_c = alt.Chart(avg_s,width=20*len(df_comps),title='Average Sentiment Scores').mark_bar().encode(
            x='Sentiment',
            y='Score',
            color='Sentiment',
            column='Competitor'
        )
        avg_c = avg_c.configure_title(fontSize=16, orient='top', anchor='middle')
        
        range_c = alt.Chart(range_s,width=20*len(df_comps),title='Range of Sentiment Scores').mark_bar().encode(
            x='Sentiment',
            y='Score',
            color='Sentiment',
            column='Competitor'
        )
        range_c = range_c.configure_title(fontSize=16, orient='top', anchor='middle')

        st.altair_chart(avg_c)
        st.altair_chart(range_c)

if __name__ == "__main__":
    main()
