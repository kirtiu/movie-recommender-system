import streamlit as st
import pickle
import pandas as pd
import gdown
import os

# ----- Custom CSS -----
st.markdown(
    """
    <style>
    body {
        background-color: #13274F;
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(120deg, #0a192f, #ffffff);
        padding: 2rem;
        border-radius: 10px;
    }
    h1 {
        color: #0d47a1;
        text-align: center;
        font-size: 3rem;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stButton>button {
        background-color: #64ffda;
        color: white;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border: none;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #64ffda;
    }
    .movie-title {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        color: #333;
        padding: 8px;
        background-color: #f9f9f9;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----- App Title -----
st.title('🎬 Movie Recommender System')

# ----- Load Data -----
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Google Drive .pkl download
file_id = "1pMP-AqImdw7SvlD-3azvhh0TYh6lXIU2"
url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists("similarity.pkl"):
    gdown.download(url, "similarity.pkl", quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----- Recommendation Logic -----
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# ----- UI Input -----
selected_movie_name = st.selectbox(
    "🎥 Type or select a movie from the dropdown",
    movies['title'].values
)

# ----- Button and Output -----
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader("📌 Recommended Movies:")
    for i in recommendations:
        st.markdown(f"<div class='movie-title'>{i}</div>", unsafe_allow_html=True)
