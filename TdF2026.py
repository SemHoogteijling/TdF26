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
from io import BytesIO
import re
import requests
import altair as alt

st.set_page_config(layout="wide")

if 'df_store_temp' not in st.session_state:
    st.session_state['df_store_temp'] = pd.DataFrame()
    

plt.rcParams['svg.fonttype'] = 'none'

@st.cache_data(ttl=3600)  # Ververst de data elke uur
def get_data(url):
    return pd.read_csv(url)

#SHEET_ID = "17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM"
#url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=638470902"
#dfTeams = pd.read_csv(url)

dfTeams = get_data(f"https://docs.google.com/spreadsheets/d/17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM/export?format=csv&gid=638470902")
dfTekst = get_data(f"https://docs.google.com/spreadsheets/d/17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM/export?format=csv&gid=592005")
dfEtappesKNF = get_data(f"https://docs.google.com/spreadsheets/d/17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM/export?format=csv&gid=1587473803")
dfEtappesUitslagen = get_data(f"https://docs.google.com/spreadsheets/d/17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM/export?format=csv&gid=450303227")
dfLogos = get_data(f"https://docs.google.com/spreadsheets/d/17zM7Xsnej3p8JjcKzxmsmH-hdsbsWx4HsmzzN8BXNVM/export?format=csv&gid=826559667")

#url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=592005"
#dfTekst = pd.read_csv(url)

#url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=1587473803"
#dfEtappesKNF = pd.read_csv(url)

#url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=450303227"
#dfEtappesUitslagen = pd.read_csv(url)

#url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=826559667"
#dfLogos = pd.read_csv(url)

#%%

teams = [
    "Team Visma", "De Kaasfabriek", "ChatGPT", "Peter Pan", "Bidonbrigade",
    "Koersklakske", "Beulen en berggeiten", "Profusion naar de top",
    "Waarom stemmen, die met de gele trui wint toch altijd",
    "Grote molen, kleine molen, laat maar lekker waaien",
    "Ja, zo kan ik het ook?!", "Teamnaam wordt geladen...", "No name",
    "Spieren voor spieren", "The Sydney Spinners", "Vlammende start",
    "Hyperscaler", "Falafel & Halloumi", "Henk", "Kijk omhoog",
    "De co-piloot", "De Vliegende Brabander", "Ik wil een gele trui",
    "In de tegenaanval", "Les dérailleurs", "L'Esprit de la Seine",
    "De mini matadoren", "Fresh Legs Momentum", "De bolletjes brigade",
    "Kopgroep zonder Kop", "Col du Futur", "Vers Bloed, Oud IJzer"
]

teams = dfTeams.columns
logos = [
    "logo1.png", "logo2.png", "logo3.png", "logo4.png",
    "logo5.png", "logo6.png", "logo7.png", "logo8.png", "logo9.png",
    "logo10.png", "logo11.png", "logo12.png", "logo13.png", "logo14.png",
    "logo15.png", "logo16.png", "logo17.png", "logo18.png", "logo19.png",
    "logo20.png", "logo21.png", "logo22.png", "logo23.png", "logo24.png",
    "logo25.png", "logo26.png", "logo27.png", "logo28.png", "logo29.png",
    "logo30.png", "logo31.png", "logo32.png","logo33.png","logo34.png"
]

teampng = dict(zip(teams, logos))


#%%
buff0,col1, buff1,col2= st.columns([.1,1,.5,8])
header = Image.open(r"header.png")
logo = Image.open(r"logo.png")

col1.image(logo, use_column_width=True)
col2.image(header, use_column_width=True)

st.write(dfTekst['Teksten'].iloc[0])
extra_tekst = dfTekst['Teksten'].iloc[1]
if isinstance(extra_tekst, str):
    st.write(extra_tekst)

etappe_tekst = dfTekst['Etappes_tekst'].dropna()
if not etappe_tekst.empty:
    st.write(etappe_tekst.iloc[-1])
    cur_etap = str(len(etappe_tekst))
else:
    cur_etap = None
    

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

            try:
                teamLogo = Image.open(teampng[top1['Team']])
                sub_kolom1, sub_kolom2,sub_kolom3 = st.columns(3)
                sub_kolom1.image(teamLogo, use_container_width=True)
            except:
                col1.write('No team logo available yet')
                
    
    with col2:
        if top2 is not None:
            st.markdown("🥈 **2e Plaats**")
            st.subheader(f"{top2['Team']}")
            st.write(f"**{top2['Totaal']} pt**")
            st.write("</div>", unsafe_allow_html=True)

            try:
                teamLogo = Image.open(teampng[top2['Team']])
                sub_kolom1, sub_kolom2,sub_kolom3 = st.columns(3)
                sub_kolom1.image(teamLogo, use_container_width=True)
            except:
                col2.write('No team logo available yet')
    
    with col3:
        if top3 is not None:
            st.markdown("🥉 **3e Plaats**")
            st.subheader(f"{top3['Team']}")
            st.write(f"**{top3['Totaal']} pt**")
            st.write("</div>", unsafe_allow_html=True)

            try:
                teamLogo = Image.open(teampng[top3['Team']])
                sub_kolom1, sub_kolom2,sub_kolom3 = st.columns(3)
                sub_kolom1.image(teamLogo, use_container_width=True)
            except:
                col3.write('No team logo available yet')
                

    st.write("---") # Visueel lijntje tussen de kaarten en de tabel
    tab.insert(0, 'Positie', range(1, len(tab) + 1))
    st.write("### Volledige Stand")
    st.table(tab, hide_index=True)

    st.write("---")
    st.write("### Scoreverloop per Etappe")
    etappe_kolommen = [col for col in dfEtappesKNF.columns if col not in ['Team', 'Totaal']]

    df_plot = dfEtappesKNF.set_index('Team')[etappe_kolommen]
    df_cumulatief = df_plot.cumsum(axis=1)
    df_grafiek = df_cumulatief.T
    df_grafiek.index = pd.CategoricalIndex(
        df_grafiek.index,
        categories=df_grafiek.index,
        ordered=True
    )
    df_reset = df_grafiek.reset_index().melt(id_vars='index', var_name='Team', value_name='Punten')
    df_reset.rename(columns={'index': 'Etappe'}, inplace=True)

    chart = alt.Chart(df_reset).mark_line().encode(
        x='Etappe',
        y='Punten',
        color='Team',
        tooltip=['Etappe', 'Team', 'Punten']
    ).properties(
        width='container',  # Breedte past zich aan de kolom aan
        height=500          # Pas dit getal aan voor de gewenste hoogte (bijv. 500 of 600)
    ).configure_legend(
        orient='bottom',
        direction='vertical',
        columns=5,
        title=None
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

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
        default = cur_etap
    )

    if etap is not None:    
        etap_int = int(etap)
        st.write('## Etappe ' + etap + ': ' + dfTekst[dfTekst['Etappe_nr']==etap_int]['Etappe_naam'].iloc[0] + ' ' + dfTekst[dfTekst['Etappe_nr']==etap_int]['Etappe_datum'].iloc[0])
        
        tab = dfEtappesUitslagen.iloc[:10, (etap_int-1)*4:(etap_int)*4]
        if not tab['Etappe'+etap].isna().any():
            etappe_tekst = dfTekst[dfTekst['Etappe_nr']==etap_int]['Etappes_tekst'].iloc[0]
            if isinstance(etappe_tekst, str):
                st.write(etappe_tekst)
            st.write("---")
            col1,col2 = st.columns(2)
            with col1:                
                st.write("### Uitslag Etappe " + etap)
                tab = dfEtappesUitslagen.iloc[:10, (etap_int-1)*4:(etap_int)*4]
                tab.columns = ['Etappe '+etap,'Punten etappe','Jongeren Bonus', 'Punten totaal']
                tab['Punten etappe'] = tab['Punten etappe'].astype(int)
                tab['Jongeren Bonus'] = tab['Jongeren Bonus'].astype('Int64')
                tab['Punten totaal'] = tab['Punten totaal'].astype(int)
                tab.insert(0, 'Positie', range(1, len(tab) + 1))
                st.table(tab,hide_index=True)
            with col2:
                st.write("### Etappe uitslag KNF Tour Teams")
                tab = dfEtappesKNF[['Team',etap]].sort_values(by=etap,ascending=False)
                tab.rename(columns={etap: 'Punten'}, inplace=True)
                tab.insert(0, 'Positie', range(1, len(tab) + 1))
                st.table(tab,hide_index=True)
        else:
            st.write('Deze etappe is nog niet gereden')


with tab3:
    st.write ("""
              # Teams
              """
              )
    allLogos = Image.open(r"allelogos (1).png")
    buff0,col1, buff1 = st.columns([1,15,1])
    col1.image(allLogos, use_column_width=True)

#    fileID = dfLogos[dfLogos['Team']=='Algemeen']['fileID'].iloc[0]
#    url = f"https://docs.google.com/uc?export=download&id={fileID}"
#    response = requests.get(url)
#    if response.status_code == 200:
#        img = Image.open(BytesIO(response.content))
#        st.image(img)
    
    buff0,col1, buff1,col2= st.columns([.1,5,1.5,5])

    with col1:
        teams = sorted(dfTeams.columns)
        radioTeam = st.selectbox('Selecteer een team:', teams, index=None, placeholder="Teams")
        if radioTeam is not None:
            dfTeam = dfTeams[[radioTeam]]
            try:
                teamLogo = Image.open(teampng[radioTeam])
                # teamLogo = Image.open(radioTeam + ".png")
                links, midden, rechts = st.columns([1, 2, 1])
                midden.image(teamLogo, use_column_width=True)
            except:
                st.write('No team logo available yet')
    if radioTeam is not None:    
        col2.table(dfTeam)

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
