import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Data Exploratory Analysis')

st.markdown("""
This app performs simple exploration of NBA player stats.
* **Python Libraries:** streamlit, pandas, base64, matplotlib, seaborn, numpy
* **Data Source:** [basketball-reference.com](https://www.basketball-reference.com/)
""")

st.sidebar.header('User Input')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2021))))

# Web scraping and some data cleaning.
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    df = df.drop(df[df.Age == 'Age'].index)  # Delete repeating headers.
    df = df.fillna(0)  # Fill na with 0.
    df = df.drop(['Rk'], axis=1)  # Drop ranking column.
    return df


player_stats = load_data(selected_year)


# Sidebar - Team Selection
teams = sorted(player_stats['Tm'].unique())
selected_team = st.sidebar.multiselect('Team', teams, teams)

# Sidebar - Position Selection
positions = ['PG', 'SG', 'SF', 'PF', 'C']
selected_position = st.sidebar.multiselect('Position', positions, positions)

# Filtering data
df_selected_team = player_stats[(player_stats['Tm'].isin(selected_team)) & (player_stats['Pos'].isin(selected_position))]

st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimensions: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
st.dataframe(df_selected_team)
