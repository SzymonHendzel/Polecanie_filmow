import pandas as pd
import numpy as np
import streamlit as st
import json
from pathlib import Path

mypath = Path().absolute()
user_json_file = Path('sample.json')
movies_dataset_path = Path('movies')
#Pobranie i ekstrakcja danych z bazy filmów
movies = pd.read_csv(f'{mypath}/Movies/movies.csv')
movies['year'] = movies['title'].str.extract('(\(\d\d\d\d\))',expand = False)
movies['year'] = movies['year'].str.extract('(\d\d\d\d)',expand=False)
movies['title'] = movies['title'].str.replace('(\(\d\d\d\d\))', '')
movies['title'] = movies['title'].apply(lambda x: x.strip())
movies['genres'] = movies['genres'].str.split(pat='|')
movies_for_user_list = movies
#koniec pobierania i ekstrakcji danych z bazy filmów

st.title("Aplikacja do polecania filmów")
with st.expander("Krótki opis aplikacji:"):
    st.write("Aplikacja ta wyświetla listę 20 filmów które powinny ci się najbardziej spodobać na podstawie filmów jakie już oglądnąłeś")

#pobieranie danych od użytkownika oraz wpisywanie ich do pliku json
with open(user_json_file) as f:
    watched_films = json.load(f)
form = st.form("my_form")
user_name = form.text_input('Wpisz nazwę użytkownika', 'user')
tittle = form.selectbox(
      'Wybierz film który oglądałeś', movies_for_user_list.title)
grade = form.number_input('Wpisz ocenę filmu',min_value = 0,max_value = 10)
sumbit = form.form_submit_button("Wpisz ocene")

if sumbit:  #warunki pobrania danych, sprawdzane jest czy yżytkownik który dodaje dane istnieje a następnie,
      if user_name not in watched_films : #sprawdzane jest czy film istnieje na liście czy nie. Nowy użytkownik tworzony jest poprzez-
        dict_of_user = {user_name:{tittle:grade}} #- funkcję dict.update
        watched_films.update(dict_of_user)
      else:
        if tittle not in watched_films[user_name]:
          watched_films[user_name][tittle] = grade
        else:
          st.write("You changed your grade")
          watched_films[user_name][tittle] = grade
with open(user_json_file, "w") as f:
        json.dump(watched_films, f)
user_movies = pd.DataFrame(watched_films[user_name].items(),columns = ['Title','Grade'])    
user_movies.set_index(keys='Title',drop=True,inplace=True)

with st.expander(f'Filmy użytkownika {user_name}'):
    st.dataframe(user_movies)


#Koniec pobierania danych od użytkownika 


#Przygotowowyanie danych do wykorzystania w algorytmie
movies_hot_encode = pd.concat([         #Hot encode wykorzysytując funkcję biblioteki pandas concat oraz funkcji applay
        movies.drop("genres", axis = 1),
        movies.genres.apply(lambda x: pd.Series(1, x)).fillna(0)
    ], axis=1, )
movies_hot_encode.drop(["movieId","year","(no genres listed)"],axis=1,inplace=True)
movies_hot_encode.set_index(keys='title',drop=True,inplace=True)
#Koniec przygotowywania danych
# Recomendation system
idx = user_movies.index.to_list()
value_list = movies_hot_encode.loc[idx,:]
user_movies_transpose = user_movies.Grade.T
genre_ratings = user_movies_transpose.dot(value_list)
genre_ratings_normalize = (genre_ratings-genre_ratings.min())/(genre_ratings.max()-genre_ratings.min())
idx2 = list(set(movies_hot_encode.index.to_list())-set(idx))
un_seen_films = movies_hot_encode.loc[idx2,:]
ratings_un_seen_films = genre_ratings_normalize*un_seen_films
ratings_un_seen_films['Avarege']=ratings_un_seen_films.sum(axis=1)
top20 = ratings_un_seen_films.loc[:,'Avarege'].sort_values(ascending = False).iloc[0:20]#wybór 20 najlepszych filmów do polecenia 
st.header("Lista 20 filmów które mogą ci się spodobać")
st.dataframe(movies.loc[movies['title'].isin(top20.index),['title','genres']].set_index('title'))
