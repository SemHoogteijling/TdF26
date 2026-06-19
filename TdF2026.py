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
import re

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
    
    st.write("""
    # Stand
    """)  
    
    # Sorteer het DataFrame op Totaal (hoog naar laag)
    tab = dfEtappesKNF[['Team','Totaal']].sort_values(by='Totaal', ascending=False)
    
    # Haal de data voor de top 3 op voor de kaarten bovenin
    # We gebruiken .get() of een check om te zorgen dat de code niet crasht als er minder dan 3 teams zijn
    top1 = tab.iloc[0] if len(tab) >= 1 else None
    top2 = tab.iloc[1] if len(tab) >= 2 else None
    top3 = tab.iloc[2] if len(tab) >= 3 else None
    
    # --- TOP 3 HIGHLIGHTS VAN LINKS NAAR RECHTS ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if top1 is not None:
            st.markdown("🥇 **1e Plaats**")
            st.subheader(f"{top1['Team']}")
            st.write(f"**{top1['Totaal']} pt**")
            st.write("</div>", unsafe_allow_html=True)
    
    with col2:
        if top2 is not None:
            st.markdown("🥈 **2e Plaats**")
            st.subheader(f"{top2['Team']}")
            st.write(f"**{top2['Totaal']} pt**")
            st.write("</div>", unsafe_allow_html=True)
    
    with col3:
        if top3 is not None:
            st.markdown("🥉 **3e Plaats**")
            st.subheader(f"{top3['Team']}")
            st.write(f"**{top3['Totaal']} pt**")
            st.write("</div>", unsafe_allow_html=True)
    
st.write("---")
st.write("### Scoreverloop per Etappe")

# 1. Pak alle etappe-kolommen (en zorg dat ze als tekst/string worden gelezen)
etappe_kolommen = [str(col).strip() for col in dfEtappesKNF.columns if str(col).strip() not in ['Team', 'Totaal']]

# 2. Sorteerfunctie voor de etappes
def robuuste_sorteer_sleutel(val):
    import re
    cijfers = re.findall(r'\d+', val)
    if cijfers:
        return (0, int(cijfers[0]))  # Cijfers eerst wiskundig ordenen
    else:
        return (1, val)              # Tekst (Algemeen klassement) sluit achteraan

etappe_kolommen_gesorteerd = sorted(etappe_kolommen, key=robuuste_sorteer_sleutel)

# 3. Bereid dataframe voor
df_tijdelijk = dfEtappesKNF.copy()
df_tijdelijk.columns = [str(col).strip() for col in df_tijdelijk.columns]

df_plot = df_tijdelijk.set_index('Team')[etappe_kolommen_gesorteerd]
df_cumulatief = df_plot.cumsum(axis=1)

# 4. Kantel de tabel
df_grafiek = df_cumulatief.T

# ==========================================
# DE OPLOSSING VOOR STREAMLIT:
# ==========================================
# Maak van de etappe-index een fysieke kolom genaamd 'Etappe'
df_grafiek = df_grafiek.reset_index().rename(columns={'index': 'Etappe'})

# Haal alle teamnamen op (dit worden de lijnen op de y-as)
team_kolommen = [col for col in df_grafiek.columns if col != 'Etappe']

# Dwing Streamlit om de handmatig gesorteerde 'Etappe' kolom te gebruiken voor de x-as
st.line_chart(
    data=df_grafiek, 
    x='Etappe', 
    y=team_kolommen
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
        tab.rename(columns={etap: 'Punten'}, inplace=True)
        st.table(tab,hide_index=True)


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
