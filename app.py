import json

import streamlit as st
import pickle
import os
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=0e9efcc811678c7890dd2f8234d3583c&language=en-US'.format(
            movie_id))

    data = response.json()
    # print(data)
    #st.write(data.get('poster_path'))
    #path = data['poster_path']
    #full_path = ("https://image.tmdb.org/t/p/w500/{}".format(path))
    #full_path = ("https://image.tmdb.org/t/p/w500/{}".format(data.get('poster_path')))

    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

    return full_path



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # now we need the sorted list
    # but if we sort the similarity them we will loose all of their index to overcome this problem
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies=[]
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch api poster
        recommended_movies_poster.append(fetch_poster(movie_id))
       # print(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_poster


# movies_list=pickle.load(open('movies.pkl','rb'))
# movies_list=movies_list['title'].values

# movies_dict=pickle.load(open('movie_dict.pkl','rb'))
#////////////////////////////////////////////////////////////////////////
pickle_file_path = 'movie_dict.pkl'  # Update with the correct file path if necessary

# Step 1: Check the file path
if not os.path.exists(pickle_file_path):
    raise FileNotFoundError(f"File '{pickle_file_path}' not found.")

# Step 2: Verify file accessibility
if not os.access(pickle_file_path, os.R_OK):
    raise PermissionError(f"No read permissions for file '{pickle_file_path}'.")

try:
    with open(pickle_file_path, 'rb') as file:
        movies_dict = pickle.load(file)
except pickle.UnpicklingError as e:
    raise ValueError(f"Error loading pickle file '{pickle_file_path}': {str(e)}")


#/////////////////////////////////////////
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie recommendation System')
movies_names=st.selectbox('Write a movie name or select from the list', movies['title'].values)


if st.button('Recommend'):
   names, poster = recommend(movies_names)
   col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
   with col1:
       st.subheader(names[0])
       st.image(poster[0])
   with col2:
       st.subheader(names[1])
       st.image(poster[1])
   with col3:
       st.subheader(names[2])
       st.image(poster[2])
   with col4:
       st.subheader(names[3])
       st.image(poster[3])
   with col5:
       st.subheader(names[4])
       st.image(poster[4])

