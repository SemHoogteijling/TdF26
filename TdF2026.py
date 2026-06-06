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
header = Image.open(r"header.png")
st.image(header, use_column_width=True)




st.write ("""
          # Teams
          """
          )


teams = dfTeams.columns


radioTeam = st.selectbox('Select team:', teams)
dfTeam = dfTeams[[radioTeam]]

st.table(dfTeam)
