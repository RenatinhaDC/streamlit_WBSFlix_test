import pandas as pd
import streamlit as st

# Load your CSV files and merge as needed
links_df = pd.read_csv('links.csv')
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
tags_df = pd.read_csv('tags.csv')

# Merging movies and ratings on 'movieId'
movie_ratings = pd.merge(movies_df, ratings_df, on='movieId')

# Merging movie_ratings and tags on 'movieId'
movie_ratings_tags = pd.merge(movie_ratings, tags_df, on='movieId')

# Print columns in the DataFrame to verify the column names
st.write("Columns in movie_ratings_tags DataFrame:", movie_ratings_tags.columns.tolist())

# Create the user-item matrix
user_item_matrix = movie_ratings_tags.pivot_table(index='userId', columns='title', values='rating', fill_value=0)

# Define function for recommendation
def item_based_recommender(movie_title, user_item_matrix, n=5):
    if movie_title not in user_item_matrix.columns:
        return "Movie not found in the database."
    
    # Calculate correlation with other movies
    similar_movies = user_item_matrix.corrwith(user_item_matrix[movie_title])

    # Sort and select top 'n' similar movies
    similar_movies = similar_movies.sort_values(ascending=False).head(n+1)[1:]

    return similar_movies

# Streamlit app for recommendations
st.title("Movie Recommender")
st.header('Find Similar Movies')

input_feature = st.text_input('Enter a movie title', '')

if input_feature:
    st.write("Your selected movie is:", input_feature)
    similar_movies = item_based_recommender(input_feature, user_item_matrix)

    if isinstance(similar_movies, pd.Series):
        st.subheader("Recommended Movies")
        st.write(similar_movies.index.tolist())
    else:
        st.write(similar_movies)