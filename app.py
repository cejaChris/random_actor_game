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
        player_name = st.text_input(label= f'Player {player}',value=f'Name')
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
    players = st.session_state['player_names']

    if 'Give Up' not in players:
        players.append('Give Up')

    
    if 'valid_actor' not in st.session_state:
        st.session_state['valid_actor'] = False

    if 'score' not in st.session_state:
        st.session_state['score'] = {
            'Actor': [],
            'Winner': []
        }

    while not st.session_state['valid_actor']:
        random_number = random.randint(1, difficulty)
        actor = game_df.loc[game_df['Rank'] == random_number]['Name'].item()

        if actor not in st.session_state['used_actors']:
            st.session_state['valid_actor'] = True
            st.session_state['current_actor'] = actor
            st.session_state['used_actors'].append(actor)


    st.header(st.session_state['current_actor'], text_alignment='center')


    winner = st.radio('Round Winner', players)
    next = st.button('Next')
    finish = st.button('Finish')
    
    if finish:
        if winner != 'Give Up':
            st.session_state['score']['Winner'].append(winner)
        else:
            st.session_state['score']['Winner'].append('N/A')

        st.session_state['score']['Actor'].append(st.session_state['current_actor'])
        st.session_state['game_section'] = 'finish'
        st.rerun()

    if next:
        if winner != 'Give Up':
            st.session_state['score']['Winner'].append(winner)
        else:
            st.session_state['score']['Winner'].append('N/A')

        st.session_state['score']['Actor'].append(st.session_state['current_actor'])
        st.session_state['valid_actor'] = False
        st.rerun()


if st.session_state['game_section'] == 'finish':
    df = pd.DataFrame(st.session_state['score'])
    st.dataframe(st.session_state['score'])
    
    new_game = st.button('New Game')

    if new_game:
        st.session_state.clear()
        st.rerun()



