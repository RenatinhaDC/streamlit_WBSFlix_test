import pandas as pd
import streamlit as st

# Title and Description
st.title("Movie Recommender")
st.subheader("Explore Popular Movies")

# Select number of most popular movies
n = st.slider("Select the number of most popular movies to display:", 0, 100, 1)
st.write("You've chosen to display", n, "popular movies.")

# Read data
links_df = pd.read_csv('links.csv')
movies_df = pd.read_csv('movies.csv')
ratings_df = pd.read_csv('ratings.csv')
tags_df = pd.read_csv('tags.csv')

# Analyze movie ratings data
ratings_mc_df = ratings_df.groupby("movieId")["rating"].agg(["mean", "count"]).reset_index()
ratings_mc_df["overall_rating"] = (ratings_mc_df["mean"] * 2) + (ratings_mc_df["count"] * 0.01)
ratings_mc_df_merged = ratings_mc_df.merge(movies_df, on="movieId", how="inner")
ratings_mc_merged_df = ratings_mc_df_merged[["movieId", "title", "genres", "mean", "count", "overall_rating"]]

# Get top N movies
top_n_movies_df = pd.DataFrame(ratings_mc_merged_df).nlargest(n, "overall_rating")
top_n_movies_df = top_n_movies_df[["title", "genres"]]
top_n_movies_df.reset_index(drop=True, inplace=True)

# Display top N movies
st.subheader(f"Top {n} Popular Movies")
st.table(top_n_movies_df)

# Merging movies and ratings on 'movieId' for recommendation
movie_ratings = pd.merge(movies_df, ratings_df, on='movieId')
movie_ratings_tags = pd.merge(movie_ratings, tags_df, on='movieId')

# Define functions for recommendation (unchanged from your code)

# Streamlit app for recommendations
with st.container():
    st.header('Find Similar Movies')

    input_feature = st.text_input('Enter a movie title', placeholder='E.g., The Matrix')

    if input_feature:
        st.write("Your selected movie is:", input_feature)
        similar_movies = item_based_recommender(movie_ratings_tags, input_feature)

        if isinstance(similar_movies, list):
            st.subheader("Recommended Movies")
            st.write(similar_movies)
        else:
            st.write(similar_movies)