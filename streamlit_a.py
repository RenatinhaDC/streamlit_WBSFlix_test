import pandas as pd
import streamlit as st

# Load data
links = pd.read_csv("links.csv")
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
tags = pd.read_csv("tags.csv")

# Merge tables
movie_ratings = pd.merge(movies, ratings, on='movieId')
movie_ratings_tags = pd.merge(movie_ratings, tags, on='movieId')

# Popularity Recommender
rating_count_df = movie_ratings_tags.groupby('movieId')['rating'].agg(['mean', 'count']).reset_index()

# Weighted Score
rating_w8t = 0.6
count_w8t = 0.4
rating_count_df['w8ed_score'] = (rating_count_df['mean'] * rating_w8t) + (rating_count_df['count'] * count_w8t)

# Top Movies
top_movies = rating_count_df.sort_values(by='w8ed_score', ascending=False).head(20)
top_movies_info = movie_ratings_tags[movie_ratings_tags['movieId'].isin(top_movies['movieId'])][movie_info_columns].drop_duplicates()
top_movies_info = top_movies_info.merge(top_movies[['movieId', 'w8ed_score']], on='movieId', how='left')

# Streamlit App
st.title("WBSFlix Recommender")
st.write("The best movie recommendations for you!")

# Display Top Movies
st.write("Top Movies:")
st.table(top_movies_info)

# Display Movie Details
selected_movie = st.selectbox("Select a movie for details:", top_movies_info['title'])
selected_movie_details = top_movies_info[top_movies_info['title'] == selected_movie]
st.write("Movie Details:")
st.table(selected_movie_details)