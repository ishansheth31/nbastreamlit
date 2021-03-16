import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Shooting Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
* **Original Code:** Chanin Nantasenamat 
""")

st.sidebar.header('Shooting User Input Features')
selected_year = st.sidebar.selectbox('Shooting Year', list(reversed(range(1950,2022))))

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_shooting.html"
    html = pd.read_html(url, header = 1)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    playerstats = raw.fillna(0)
    playerstats = playerstats.drop(['Rk'], axis=1)
    playerstats = playerstats.drop(["Unnamed: 9"], axis=1)
    playerstats = playerstats.drop(["Unnamed: 16"], axis=1)
    playerstats = playerstats.drop(["Unnamed: 23"], axis=1)
    playerstats = playerstats.drop(["Unnamed: 26"], axis=1)
    playerstats = playerstats.drop(["Unnamed: 29"], axis=1)
    playerstats = playerstats.drop(["Unnamed: 32"], axis=1)
    playerstats = playerstats.rename(columns={'2P.1': '2P%'})
    playerstats = playerstats.rename(columns={'0-3.1': '0-3 %'})
    playerstats = playerstats.rename(columns={'3-10.1': '3-10 %'})
    playerstats = playerstats.rename(columns={'10-16.1': '10-16 %'})
    playerstats = playerstats.rename(columns={'16-3P.1': '16-3P %'})
    playerstats = playerstats.rename(columns={'3P.1': '3P%'})
    playerstats = playerstats.rename(columns={'2P.2': '2P Assisted %'})
    playerstats = playerstats.rename(columns={'3P.2': '3P Assisted %'})
    playerstats = playerstats.rename(columns={'%3PA': '% Corner 3s Attempted'})
    playerstats = playerstats.rename(columns={'%3P': 'Corner 3P%'})
    playerstats = playerstats.rename(columns={'#': '# Dunks'})
    playerstats = playerstats.rename(columns={'Att.': '# Attempted Heaves'})                                          
    playerstats = playerstats.rename(columns={'#.1': '# Made Heaves'})
    for col in playerstats.columns[4:]:
        playerstats = playerstats.astype({'Age': 'int64', 'G': 'int64', col: 'float'})
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Shooting Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Shooting Position', unique_pos, unique_pos)

sorted_unique_minutes = sorted(playerstats.MP.unique())
selected_minutes_min, selected_minutes_max = st.sidebar.select_slider('Shooting Minutes', sorted_unique_minutes, (min(sorted_unique_minutes), max(sorted_unique_minutes)))

sorted_unique_games = sorted(playerstats.G.unique())
selected_games_min, selected_games_max = st.sidebar.select_slider('Shooting Games Played', sorted_unique_games, (min(sorted_unique_games), max(sorted_unique_games)))

if st.sidebar.checkbox("Shooting Pick Specific Players"):
    sorted_unique_player = sorted(playerstats.Player.unique())
    selected_player = st.sidebar.multiselect("Shooting Select Player", sorted_unique_player, None)
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MP.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.G.between((selected_games_min), (selected_games_max))) &  (playerstats.Player.isin(selected_player))] 
else:
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MP.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.G.between((selected_games_min), (selected_games_max)))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)
#

st.header('Statistical Scatterpolot Generator')
st.markdown("String types (Pos/Tm) only work for scatter/hist plots")

list1 = []
for columns in df_selected_team.columns[1:]:
    list1.append(columns)

list2 = ['scatter', 'kde', 'hist', 'hex', 'reg', 'resid']
    
    
x_axis = st.selectbox("Shooting Select X-Axis", list1) 
y_axis = st.selectbox("Shooting Select Y-Axis", list1) 
type1 = st.selectbox("Shooting Select Graph Type", list2) 
x1 = df_selected_team[str(x_axis)]
y1 = df_selected_team[str(y_axis)]
t1 = str(type1)

sns.jointplot(x1, y1, kind=t1)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()