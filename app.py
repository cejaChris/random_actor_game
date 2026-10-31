import streamlit as st
import pandas as pd
import random

# streamlit run app.py

actor_df = pd.read_csv('./top_1000_grossing_actors.csv')
difficulties = {
    'Easy': 50,
    'Medium': 100,
    'Hard': 250,
    'Nerd': 1000
}

st.set_page_config(layout="wide")

if 'used_actors' not in st.session_state:
    st.session_state['used_actors'] = []

if 'game_section' not in st.session_state:
    st.session_state['game_section'] = 'not_started'

if st.session_state['game_section'] == 'not_started':
    st.header('Letterboxd Actor Game', text_alignment='center')
    players = st.slider('Players', 1, 10)
    next = st.button('Next')

    if next:
        st.session_state['player_count'] = players
        st.session_state['game_section'] = 'naming_players'
        st.rerun()

if st.session_state['game_section'] == 'naming_players':
    players = st.session_state['player_count']
    player_list = list(range(1, players + 1))
    player_names = []

    for player in player_list:
        player_name = st.text_input(f'Player {player} Name', value=f'Player {player}')
        player_names.append(player_name)
    
    done = st.button('Done')

    if done:
        st.session_state['player_names'] = player_names
        st.session_state['game_section'] = 'difficulty'
        st.rerun()

if st.session_state['game_section'] == 'difficulty':
    difficulty = st.radio('Difficulty', ['Easy', 'Medium', 'Hard', 'Nerd'])
    start = st.button('Start Game')

    if start:
        st.session_state['difficulty'] = difficulties[difficulty]
        st.session_state['game_section'] = 'ready'
        st.rerun()

if st.session_state['game_section'] == 'ready':
    difficulty = st.session_state['difficulty']
    game_df = actor_df.loc[actor_df['Rank'] <= difficulty]

    valid_actor = False

    while not valid_actor:
        random_number = random.randint(1, difficulty)
        actor = game_df.loc[game_df['Rank'] == random_number]['Name'].item()

        if actor not in st.session_state['used_actors']:
            valid_actor = True

    st.header(actor, text_alignment='center')



