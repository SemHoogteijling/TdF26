# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:38:20 2023

@author: shoogtei


"""

import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import copy
import time
from PIL import Image

st.set_page_config(layout="wide")

if 'df_store_temp' not in st.session_state:
    st.session_state['df_store_temp'] = pd.DataFrame()
    

plt.rcParams['svg.fonttype'] = 'none'

SHEET_ID = "17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

dfTeams = pd.read_csv(url)

#%%
buff0,col1, buff1,col2= st.columns([.1,1,.5,8])
header = Image.open(r"header.png")
logo = Image.open(r"logo.png")

col1.image(logo, use_column_width=True)
col2.image(header, use_column_width=True)


tab1, tab2, tab3 = st.tabs(["Stand", "Etappes", "Teams"])

with tab1:
  st.write ("""
            # Stand
            """
            )  
    
with tab2:    
    st.write ("""
              # Etappes
              """
              )
    
    etap = st.segmented_control(
        "Etappes",
        options=[str(i) for i in range(1, 22)],
        # format_func=lambda option: option_map[option],
        selection_mode="single",
    )

    st.write ("""
              Nog geen uitslagen bekend van deze etappe.
              """
              )


with tab3:
    st.write ("""
              # Teams
              """
              )
    buff0,col1, buff1,col2= st.columns([.1,5,3,5])
    
    teams = dfTeams.columns
    radioTeam = col1.selectbox('Select team:', teams)
    dfTeam = dfTeams[[radioTeam]]
    
    col2.table(dfTeam)
    
    teamLogo = Image.open(radioTeam + ".png")
    col1.image(teamLogo, use_column_width=True)
