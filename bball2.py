import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('2021 NBA Backpicks Stats')


st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [https://backpicks.com/metrics/2021-players/](https://backpicks.com/metrics/2021-players/)
* **Original Code:** Chanin Nantasenamat 
""")

st.sidebar.header('Backpicks User Input Features')
#
## Web scraping of NBA player stats
#@st.cache
html = pd.read_html('https://backpicks.com/metrics/2021-players/')
playerstats = html[0]
playerstats = playerstats.rename(columns={'rTS%': 'rTS'})
playerstats['rTS'] = playerstats['rTS'].map(lambda x: x.lstrip().rstrip('%'))
playerstats = playerstats.astype({'rTS': 'float64'})
playerstats['rLayup Ast%'] = playerstats['rLayup Ast%'].map(lambda x: x.lstrip().rstrip('%'))
playerstats = playerstats.astype({'rLayup Ast%': 'float64'})
playerstats['cTOV%'] = playerstats['cTOV%'].map(lambda x: x.lstrip().rstrip('%'))
playerstats = playerstats.astype({'cTOV%': 'float64'})
playerstats['Rim FG%'] = playerstats['Rim FG%'].map(lambda x: x.lstrip().rstrip('%'))
playerstats = playerstats.astype({'Rim FG%': 'float64'})
#playerstats['Midrange FG%'] = playerstats['Midrange FG%'].map(lambda x: x.lstrip().rstrip('%'))
#playerstats = playerstats.astype({'Midrange FG%': 'float64'})
playerstats['Midrange FG%'] = playerstats['Midrange FG%'].str.replace(r'\D', '').astype(float)
playerstats = playerstats.drop(['FT%'], axis=1)

#
#
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

sorted_unique_games = sorted(playerstats.GP.unique())
selected_games_min, selected_games_max = st.sidebar.select_slider('Games Played', sorted_unique_games, (min(sorted_unique_games), max(sorted_unique_games)))

sorted_unique_obpm = sorted(playerstats.OBPM.unique())
selected_obpm_min, selected_obpm_max = st.sidebar.select_slider('Offensive BPM', sorted_unique_obpm, (min(sorted_unique_obpm), max(sorted_unique_obpm)))

sorted_unique_bpm = sorted(playerstats.BPM.unique())
selected_bpm_min, selected_bpm_max = st.sidebar.select_slider('BPM', sorted_unique_bpm, (min(sorted_unique_bpm), max(sorted_unique_bpm)))

sorted_unique_ts = sorted(playerstats.rTS.unique())
selected_ts_min, selected_ts_max = st.sidebar.select_slider('Relative True Shooting %', sorted_unique_ts, (min(sorted_unique_ts), max(sorted_unique_ts)))

if st.sidebar.checkbox("Pick Specific Players for Backpicks"):
    sorted_unique_player = sorted(playerstats.Player.unique())
    selected_player = st.sidebar.multiselect("Select Player", sorted_unique_player, None)
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Player.isin(selected_player)) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.GP.between((selected_games_min), (selected_games_max))) & (playerstats.rTS.between((selected_ts_min), (selected_ts_max)))] 
else:
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.GP.between((selected_games_min), (selected_games_max))) & (playerstats.rTS.between((selected_ts_min), (selected_ts_max)))] 


st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

list1 = []
for columns in df_selected_team.columns[1:]:
    list1.append(columns)

list2 = ['scatter', 'kde', 'hist', 'hex', 'reg', 'resid']

st.header('Statistical Scatterpolot Generator')
st.markdown("String types (Pos/Tm/Midrange FG%) only work for scatter/hist plots")

x_axis = st.selectbox("Select X-Axis", list1) 
y_axis = st.selectbox("Select Y-Axis", list1) 
type1 = st.selectbox("Select Backpics Graph Type", list2) 
x1 = df_selected_team[str(x_axis)]
y1 = df_selected_team[str(y_axis)]
t1 = str(type1)

sns.jointplot(x1, y1, kind=t1)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.markdown("""
Legend:
    
* BPM = Backpicks Box plus-minus model.
* OBPM = Offensive Box plus-minus.
* ScoreVal = Scoring value, an estimate of a player’s points per 100 impact from scoring only.
* PlayVal = Playmaking value, an estimate of a player’s points per 100 impact from playmaking only.
* Load = offensive load, an estimate of the number of a player a player is “directly involved” in on offense every 100 possessions.
* rTS% = relative True Shooting percentage (true shooting compared to league average). Note that this uses real true shooting and not an estimation.
* Box Creation = An estimate of shots created for teammates per 100 possessions.
* Passer Rating = An estimate of a player’s passing ability on (approximately) a 1-10 scale.
* 3p% Pro = 3-point proficiency, a combination of 3-point volume and accuracy.
* Spacing = A basic estimate of player spacing using.
* cTOV% = creation-adjusted turnover rate, or turnovers committed as a percentage of offensive load.
* FD = Fouls draw per 75 possessions
* FTA = Free throw attempts per 75 possessions
* FTOV = Forced Turnovers (steals + charges drawn + offensive fouls drawn) per 75
* Midrange FGA = midrange shots per 75 possessions
* Rim + FT TSA% = Percentage of overall true shot attempts (FGA+FTA) that are at the rim or from free throws
* Corner 3 Share = Percentage of a player’s 3-point attempts that come from corner 3s
""")


