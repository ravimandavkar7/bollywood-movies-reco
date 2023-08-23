import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movies_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movies_id)
)
    data=response.json()
    if 'poster_path' in data and data['poster_path'] is not None:
        poster_path = data['poster_path']
        return "https://image.tmdb.org/t/p/w185/" + poster_path
    else:
        return "https://image.tmdb.org/t/p/w185//NoImage.jpg"




def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies=[]
    recommend_movies_poster=[]
    for i in movies_list:
        movies_id=movies.iloc[i[0]].imdbId
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        poster_url=fetch_poster(movies_id)
        if poster_url != "No Poster Available":
            recommend_movies_poster.append(poster_url)

    return recommend_movies,recommend_movies_poster

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)

    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
