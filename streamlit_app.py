from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

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

def main():
    st.set_page_config(page_title='Calibre') #layout='wide', initial_sidebar_state='auto'
    sep = '<|endoftext|>'
    main_txt = """Calibre"""
    sub_txt = "Competitor Analysis"
    display_app_header(main_txt,sub_txt,is_sidebar = False)
    
if __name__ == "__main__":
    main()
