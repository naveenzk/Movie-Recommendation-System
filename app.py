import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

@st.cache_data
def load_data():
    try:
        movies = pd.read_csv("movies.csv")
    except FileNotFoundError:
        st.error("Could not find `movies.csv`. Make sure it's in the same folder.")
        st.stop()
    movies = movies.dropna(subset=['title']).reset_index(drop=True)
    return movies

def fetch_poster(movie_title):
    if not TMDB_API_KEY:
        st.error("TMDB API key is missing. Please check your `.env` file.")
        return None
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    if data.get('results'):
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

def recommend(movie_title, movies, similarity, num_recs=20):
    match = movies[movies['title'].str.lower() == movie_title.lower()]
    if match.empty:
        return [], []
    movie_idx = match.index[0]
    distances = similarity[movie_idx]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recs+1]  # Skip itself
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_name = movies.iloc[i[0]].title
        poster_url = fetch_poster(movie_name)
        recommended_movies.append(movie_name)
        recommended_posters.append(poster_url)
    return recommended_movies, recommended_posters

@st.cache_data(ttl=86400)
def get_genre_id_map():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    genre_map = {}
    for genre in data.get('genres', []):
        genre_map[genre['name'].lower()] = genre['id']
    return genre_map

@st.cache_data(ttl=3600)
def fetch_popular_movies_by_genre(genre_id, num_movies=20):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc&language=en-US&page=1"
    response = requests.get(url)
    data = response.json()
    movies = []
    posters = []
    for movie in data.get('results', [])[:num_movies]:
        movies.append(movie['title'])
        poster_path = movie.get('poster_path')
        if poster_path:
            posters.append(f"https://image.tmdb.org/t/p/w500{poster_path}")
        else:
            posters.append("https://via.placeholder.com/200x300?text=No+Image")
    return movies, posters

st.set_page_config(page_title="🎥 Movie Recommender", layout="wide")
st.markdown("<h1 style='text-align: center; color: #320A6B;'>Movie Recommendation System</h1>", unsafe_allow_html=True)

movies = load_data()

try:
    similarity = pickle.load(open("similarity.pkl", "rb"))
except FileNotFoundError:
    st.error("Missing `similarity.pkl`. Please make sure it's in the folder.")
    st.stop()

# Initialize session state for last recommended movie (if not exists)
if 'last_recommended_movie' not in st.session_state:
    st.session_state.last_recommended_movie = None

col1, col2 = st.columns([5, 1])
with col1:
    selected_movie_name = st.selectbox(
        "Search and select a movie:",
        movies['title'].values,
        index=None,
        placeholder="Type to search..."
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_clicked = st.button("Recommend Movies", key="recommend_button")

if recommend_clicked and selected_movie_name:
    st.session_state.last_recommended_movie = selected_movie_name

genres = ["Recommended", "Horror", "Comedy", "Action", "Romance", "Drama", "Thriller", "Adventure", "Animation", "Family"]
genre_map = get_genre_id_map()
tabs = st.tabs(genres)

for genre, tab in zip(genres, tabs):
    with tab:
        if genre == "Recommended":
            if st.session_state.last_recommended_movie:
                names, posters = recommend(st.session_state.last_recommended_movie.strip(), movies, similarity, num_recs=20)
                if names:
                    st.subheader(f"Because you liked **{st.session_state.last_recommended_movie}**, you might also enjoy:")
                    cols_per_row = 5
                    for row_start in range(0, len(names), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for idx, col in enumerate(cols):
                            movie_index = row_start + idx
                            if movie_index < len(names):
                                with col:
                                    st.image(
                                        posters[movie_index] if posters[movie_index] else "https://via.placeholder.com/200x300?text=No+Image",
                                        use_container_width=True
                                    )
                                    st.markdown(
                                        f"<div style='text-align: center; font-size: 14px;'>{names[movie_index]}</div>",
                                        unsafe_allow_html=True
                                    )
                else:
                    st.warning("No recommendations found. Please check the spelling or try another movie.")
            else:
                st.info("Search and select a movie, then click 'Recommend Movies' to see recommendations here.")
        else:
            genre_id = genre_map.get(genre.lower())
            if genre_id:
                names, posters = fetch_popular_movies_by_genre(genre_id, num_movies=20)
                if names:
                    cols_per_row = 5
                    for row_start in range(0, len(names), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for idx, col in enumerate(cols):
                            movie_index = row_start + idx
                            if movie_index < len(names):
                                with col:
                                    st.image(
                                        posters[movie_index],
                                        use_container_width=True
                                    )
                                    st.markdown(
                                        f"<div style='text-align: center; font-size: 14px;'>{names[movie_index]}</div>",
                                        unsafe_allow_html=True
                                    )
                else:
                    st.warning(f"No popular movies found for genre {genre}.")
            else:
                st.warning(f"Genre ID not found for {genre}.")
