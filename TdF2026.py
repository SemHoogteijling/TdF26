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
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=638470902"
dfTeams = pd.read_csv(url)

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=592005"
dfTekst = pd.read_csv(url)

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1587473803"
dfEtappesKNF = pd.read_csv(url)

#%%
buff0,col1, buff1,col2= st.columns([.1,1,.5,8])
header = Image.open(r"header.png")
logo = Image.open(r"logo.png")

col1.image(logo, use_column_width=True)
col2.image(header, use_column_width=True)

st.write (dfTekst['Teksten'].iloc[0])

tab1, tab2, tab3, tab4 = st.tabs(["Stand", "Etappes", "Teams","Uitleg"])

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

    if etap is not None:
        etap_int = int(etap)
        st.write('## Etappe ' + etap + ': ' + dfTekst[dfTekst['Etappe_nr']==etap_int]['Etappe_naam'].iloc[0])
        st.write(dfTekst[dfTekst['Etappe_nr']==etap_int]['Etappes_tekst'].iloc[0])
        tab = dfEtappesKNF[['Team',etap]].sort_values(by=etap,ascending=False)
        st.table(tab.style.hide(axis='index'))


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

    try:
        teamLogo = Image.open(radioTeam + ".png")
        col1.image(teamLogo, use_column_width=True)
    except:
        col1.write('No team logo available yet')


with tab4:
    st.write("""
    We gaan terug naar de basis: je mag 7 renners kiezen die punten opleveren in de dag top-10:
    
    * **nr. 1** - 12 punten
    * **nr. 2** - 10
    * **nr. 3** - 8
    * **nr. 4** - 7
    * **nr. 5** - 6
    * **nr. 6** - 5
    * **nr. 7** - 4
    * **nr. 8** - 3
    * **nr. 9** - 2
    * **nr. 10** - 1
    
    En het eindklassement van de gele trui nr 1 tot nr 10:  
    **45 - 37 - 29 - 25 - 21 - 17 - 13 - 9 - 5 - 1**
    
    Het thema dit jaar is natuurlijk **‘The Youth Takes Over’** (zou Frankrijk echt weer een Tourheld krijgen?). Daarom verdient elke renner in je team die meedoet met het jongerenklassement (<= 25 jaar), **5 bonuspunten** als hij zich in een top 10 rijdt.
    """)
