import pandas as pd
import numpy as np
import streamlit as st
import json

movies = pd.read_csv('../Aplikacja polecania/Movies/movies.csv')
ratings = pd.read_csv('../Aplikacja polecania/Movies/ratings.csv')
movies['year'] = movies['title'].str.extract('(\(\d\d\d\d\))',expand = False)
movies['year'] = movies['year'].str.extract('(\d\d\d\d)',expand=False)
movies['title'] = movies['title'].str.replace('(\(\d\d\d\d\))', '')
movies['title'] = movies['title'].apply(lambda x: x.strip())
movies['genres'] = movies['genres'].str.split(pat='|')
movies_for_user_list = movies
with open('../Aplikacja polecania\sample.json') as f:
    watched_films = json.load(f)
form = st.form("my_form")
tittle = form.selectbox(
      'Wybierz film który oglądałeś', movies_for_user_list.title)
grade = form.number_input('Wpisz ocenę filmu',min_value = 0,max_value = 10)

# Now add a submit button to the form:
sumbit = form.form_submit_button("Wpisz ocene")

if sumbit:
      if tittle not in watched_films :
        watched_films[tittle] = grade
      else:
        st.write("You changed your grade")
        watched_films[tittle] = grade
with open('../Aplikacja polecania/sample.json', "w") as f:
        json.dump(watched_films, f)
user_movies = pd.DataFrame(watched_films.items(),columns = ['Title','Grade'])    
user_movies.set_index(keys='Title',drop=True,inplace=True)
st.dataframe(user_movies)
#watched_films mogę połączyć z movies przy pomocy innerjoina na podstawie tytułów bo one są unikalne.



movies_hot_encode = pd.concat([             #Hot encode wykorzysytując funkcję biblioteki pandas concat oraz funkcji applay
        movies.drop("genres", axis = 1),
        movies.genres.apply(lambda x: pd.Series(1, x)).fillna(0)
    ], axis=1, )
movies_hot_encode.drop(["movieId","year","(no genres listed)"],axis=1,inplace=True)
movies_hot_encode.set_index(keys='title',drop=True,inplace=True)
# Recomendation system
idx = user_movies.index.to_list()
value_list = movies_hot_encode.loc[idx,:]
user_movies_transpose = user_movies.T
genre_ratings = user_movies_transpose.dot(value_list)
genre_ratings_normalize = (genre_ratings-genre_ratings.min())/(genre_ratings.max()-genre_ratings.min())
idx2 = list(set(movies_hot_encode.index.to_list())-set(idx))
un_seen_films = movies_hot_encode.loc[idx2,:]
ratings_un_seen_films = genre_ratings_normalize*un_seen_films
ratings_un_seen_films['Avarege']=ratings_un_seen_films.sum(axis=1)
top20 = ratings_un_seen_films.loc[:,'Avarege'].sort_values(ascending = False).iloc[0:20]#wybór 20 najlepszych filmów do polecenia 
st.dataframe(movies.loc[movies['title'].isin(top20.index),:])
