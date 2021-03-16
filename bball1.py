import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
* **Original Code:** Chanin Nantasenamat 
""")

st.sidebar.header('General User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2022))))

@st.cache
def load_data(year):
    url1 = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_advanced.html"
    html1 = pd.read_html(url1, header = 0)
    df = html1[0]
    raw1 = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw1 = raw1.fillna(0)
    playerstats1 = raw1.drop(['Rk'], axis=1)
    playerstats1 = playerstats1.drop(["Unnamed: 19"], axis=1)
    playerstats1 = playerstats1.drop(["Unnamed: 24"], axis=1)
    url2 = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html2 = pd.read_html(url2, header = 0)
    df2 = html2[0]
    raw2 = df2.drop(df2[df2.Age == 'Age'].index) # Deletes repeating headers in content
    raw2 = raw2.fillna(0)
    playerstats2 = raw2.drop(['Rk'], axis=1)
    playerstats = pd.merge(playerstats2, playerstats1, on=["Player", "Pos", "Tm", "Age", "G"])
    playerstats = playerstats.drop(["MP_y"], axis=1)
    playerstats = playerstats.rename(columns={'MP_x': 'MPG'})
    playerstats = playerstats.rename(columns={'TS%': 'TS'})
    for col in playerstats.columns[5:]:
        playerstats = playerstats.astype({'Age': 'int64', 'G': 'int64', 'GS': 'int64', col: 'float'})
    return playerstats
playerstats = load_data(selected_year)

sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

unique_pos = ['PG','SG','SF','PF','C']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

sorted_unique_minutes = sorted(playerstats.MPG.unique())
selected_minutes_min, selected_minutes_max = st.sidebar.select_slider('Minutes', sorted_unique_minutes, (min(sorted_unique_minutes), max(sorted_unique_minutes)))

sorted_unique_games = sorted(playerstats.G.unique())
selected_games_min, selected_games_max = st.sidebar.select_slider('Games Played', sorted_unique_games, (min(sorted_unique_games), max(sorted_unique_games)))

sorted_unique_points = sorted(playerstats.PTS.unique())
selected_points_min, selected_points_max = st.sidebar.select_slider('Points', sorted_unique_points, (min(sorted_unique_points), max(sorted_unique_points)))

sorted_unique_assists = sorted(playerstats.AST.unique())
selected_assists_min, selected_assists_max = st.sidebar.select_slider('Assists', sorted_unique_assists, (min(sorted_unique_assists), max(sorted_unique_assists)))

sorted_unique_rebounds = sorted(playerstats.TRB.unique())
selected_rebounds_min, selected_rebounds_max = st.sidebar.select_slider('Rebounds', sorted_unique_rebounds, (min(sorted_unique_rebounds), max(sorted_unique_rebounds)))

sorted_unique_obpm = sorted(playerstats.OBPM.unique())
selected_obpm_min, selected_obpm_max = st.sidebar.select_slider('Offensive BPM', sorted_unique_obpm, (min(sorted_unique_obpm), max(sorted_unique_obpm)))

sorted_unique_dbpm = sorted(playerstats.DBPM.unique())
selected_dbpm_min, selected_dbpm_max = st.sidebar.select_slider('Defensive BPM', sorted_unique_dbpm, (min(sorted_unique_dbpm), max(sorted_unique_dbpm)))

sorted_unique_bpm = sorted(playerstats.BPM.unique())
selected_bpm_min, selected_bpm_max = st.sidebar.select_slider('BPM', sorted_unique_bpm, (min(sorted_unique_bpm), max(sorted_unique_bpm)))

sorted_unique_ts = sorted(playerstats.TS.unique())
selected_ts_min, selected_ts_max = st.sidebar.select_slider('True Shooting %', sorted_unique_ts, (min(sorted_unique_ts), max(sorted_unique_ts)))


if st.sidebar.checkbox("Pick Specific Players"):
    sorted_unique_player = sorted(playerstats.Player.unique())
    selected_player = st.sidebar.multiselect("Select Player", sorted_unique_player, None)
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MPG.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.PTS.between((selected_points_min), (selected_points_max))) & (playerstats.AST.between((selected_assists_min), (selected_assists_max))) & (playerstats.TRB.between((selected_rebounds_min), (selected_rebounds_max))) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.DBPM.between((selected_dbpm_min), (selected_dbpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.G.between((selected_games_min), (selected_games_max))) & (playerstats.TS.between((selected_ts_min), (selected_ts_max))) & (playerstats.Player.isin(selected_player))] 
else:
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MPG.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.PTS.between((selected_points_min), (selected_points_max))) & (playerstats.AST.between((selected_assists_min), (selected_assists_max))) & (playerstats.TRB.between((selected_rebounds_min), (selected_rebounds_max))) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.DBPM.between((selected_dbpm_min), (selected_dbpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.G.between((selected_games_min), (selected_games_max))) & (playerstats.TS.between((selected_ts_min), (selected_ts_max)))] 
    
st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

list1 = []
for columns in df_selected_team.columns[1:]:
    list1.append(columns)

list2 = ['scatter', 'kde', 'hist', 'hex', 'reg', 'resid']

st.header('Statistical Scatterpolot Generator')
st.markdown("String types (Pos/Tm) only work for scatter/hist plots")

    
    
x_axis = st.selectbox("Select X-Axis", list1) 
y_axis = st.selectbox("Select Y-Axis", list1) 
type1 = st.selectbox("Select Graph Type", list2) 
x1 = df_selected_team[str(x_axis)]
y1 = df_selected_team[str(y_axis)]
t1 = str(type1)

sns.jointplot(x1, y1, kind=t1)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()