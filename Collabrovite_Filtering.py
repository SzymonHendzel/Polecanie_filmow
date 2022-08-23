import pandas as pd
import numpy as np
import streamlit as st
import json

movies = pd.read_csv('E:\Data_scientist/Linear_regression/data_set/Movies/movies.csv')
ratings = pd.read_csv('E:\Data_scientist/Linear_regression/data_set/Movies/ratings.csv')
with open('E:Data_scientist/Linear_regression/sample.json') as f:
    watched_films = json.load(f)
form = st.form("my_form")
tittle = form.selectbox(
      'Wybierz film który oglądałeś', movies.title)
grade = form.number_input('Wpisz ocenę filmu',min_value = 0,max_value = 10)

# Now add a submit button to the form:
sumbit = form.form_submit_button("Wpisz ocene")

if sumbit:
      if tittle not in watched_films :
        watched_films[tittle] = grade
      else:
        st.write("You changed your grade")
        watched_films[tittle] = grade
with open('E:Data_scientist/Linear_regression/sample.json', "w") as f:
        json.dump(watched_films, f)
    
st.dataframe(pd.DataFrame(watched_films.items(),columns = ['Tittle','Grade']))
#watched_films mogę połączyć z movies przy pomocy innerjoina na podstawie tytułów bo one są unikalne.

