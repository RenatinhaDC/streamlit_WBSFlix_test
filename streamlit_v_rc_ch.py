import pandas as pd
import streamlit as st

# Load data
movie_ratings_tags = pd.read_csv("movie_ratings_tags.csv")
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
tags = pd.read_csv("tags.csv")

# Merging movies and ratings on 'movieId'
movie_ratings = pd.merge(movies, ratings, on='movieId')

# Merging movie_ratings and tags on 'movieId'
movie_ratings_tags = pd.merge(movie_ratings, tags, on='movieId')


# Define functions

def get_sparse_matrix(data: pd.DataFrame):
    return data.pivot_table(values='rating', index='userId_x', columns='title', fill_value=0)

def item_based_recommender(data: pd.DataFrame, title: str, n: int = 5):
    sparse_matrix = get_sparse_matrix(data)
    
    if title not in sparse_matrix.columns:
        return "Movie not found in the database."

    similar_movies = (
        sparse_matrix.corrwith(sparse_matrix[title])
        .sort_values(ascending=False)
        .index
        .to_list()[1:n+1]
    )
    return similar_movies


# Streamlit app

becouse_you_like = st.container()

with becouse_you_like:
    st.header('Similar Movies Recommendation')
    
    input_feature = st.text_input('Enter a movie title', '')  # Get user input
    
    if input_feature:
        st.write("Your selected movie is:", input_feature)
        similar_movies = item_based_recommender(movie_ratings_tags, input_feature)
        
        if isinstance(similar_movies, list):
            st.write("Recommended movies:")
            st.write(similar_movies)
        else:
            st.write(similar_movies)