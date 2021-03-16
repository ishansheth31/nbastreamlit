import streamlit as st
from multiapp import MultiApp

def bball1():
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
    
    st.sidebar.header('User Input Features')
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
    
    sorted_unique_age = sorted(playerstats.Age.unique())
    selected_age_min, selected_age_max = st.sidebar.select_slider('Age', sorted_unique_age, (min(sorted_unique_age), max(sorted_unique_age)))
    
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
        df_selected_team = playerstats[(playerstats.Age.between((selected_age_min), (selected_age_max))) & (playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MPG.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.PTS.between((selected_points_min), (selected_points_max))) & (playerstats.AST.between((selected_assists_min), (selected_assists_max))) & (playerstats.TRB.between((selected_rebounds_min), (selected_rebounds_max))) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.DBPM.between((selected_dbpm_min), (selected_dbpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.G.between((selected_games_min), (selected_games_max))) & (playerstats.TS.between((selected_ts_min), (selected_ts_max))) & (playerstats.Player.isin(selected_player))] 
    else:
        df_selected_team = playerstats[(playerstats.Age.between((selected_age_min), (selected_age_max))) & (playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos)) & (playerstats.MPG.between((selected_minutes_min), (selected_minutes_max))) & (playerstats.PTS.between((selected_points_min), (selected_points_max))) & (playerstats.AST.between((selected_assists_min), (selected_assists_max))) & (playerstats.TRB.between((selected_rebounds_min), (selected_rebounds_max))) & (playerstats.OBPM.between((selected_obpm_min), (selected_obpm_max))) & (playerstats.DBPM.between((selected_dbpm_min), (selected_dbpm_max))) & (playerstats.BPM.between((selected_bpm_min), (selected_bpm_max))) & (playerstats.G.between((selected_games_min), (selected_games_max))) & (playerstats.TS.between((selected_ts_min), (selected_ts_max)))] 
        
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

def bball2():
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
    
    st.sidebar.header('User Input Features')
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
    
    if st.sidebar.checkbox("Pick Specific Players"):
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

def bball3():

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
    
    st.sidebar.header('User Input Features')
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2022))))
    
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
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)
    
    # Sidebar - Position selection
    unique_pos = ['C','PF','SF','PG','SG']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)
    
    sorted_unique_minutes = sorted(playerstats.MP.unique())
    selected_minutes_min, selected_minutes_max = st.sidebar.select_slider('Minutes', sorted_unique_minutes, (min(sorted_unique_minutes), max(sorted_unique_minutes)))
    
    sorted_unique_games = sorted(playerstats.G.unique())
    selected_games_min, selected_games_max = st.sidebar.select_slider('Games Played', sorted_unique_games, (min(sorted_unique_games), max(sorted_unique_games)))
    
    if st.sidebar.checkbox("Pick Specific Players"):
        sorted_unique_player = sorted(playerstats.Player.unique())
        selected_player = st.sidebar.multiselect("Select Player", sorted_unique_player, None)
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
        
        
    x_axis = st.selectbox("Select X-Axis", list1) 
    y_axis = st.selectbox("Select Y-Axis", list1) 
    type1 = st.selectbox("Select Graph Type", list2) 
    x1 = df_selected_team[str(x_axis)]
    y1 = df_selected_team[str(y_axis)]
    t1 = str(type1)
    
    sns.jointplot(x1, y1, kind=t1)
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

app = MultiApp()
app.add_app("General Stats", bball1)
app.add_app("2021 Backpicks Advanced Metrics", bball2)
app.add_app("Shooting Stats", bball3)
app.run()