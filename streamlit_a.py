# Import necessary libraries
import pandas as pd
import streamlit as st

# Function to get top recommendations
def get_top_n_recommendations(movie_title, n, movies_cosines_matrix, user_movie_matrix, movie_ratings_tags):
    # Find the movieId for the given movie title
    title_column_name = 'title'

    # Check if the title column exists in the DataFrame
    if title_column_name not in movie_ratings_tags.columns:
        raise KeyError(f"Column '{title_column_name}' not found in movie_ratings_tags DataFrame.")

    # Find the movieId for the given movie title
    movieId = movie_ratings_tags[movie_ratings_tags[title_column_name].str.contains(movie_title, case=False)]['movieId'].values[0]

    # Creating a DataFrame using the values from 'movies_cosines_matrix' for the input 'movieId'.
    movie_cosines_df = pd.DataFrame(movies_cosines_matrix.iloc[movies_cosines_matrix.index.get_loc(movieId)])

    # Renaming the column to 'cosine_similarity'
    movie_cosines_df = movie_cosines_df.rename(columns={movieId: 'cosine_similarity'})

    # Removing the row with the index 'movieId'
    movie_cosines_df = movie_cosines_df[movie_cosines_df.index != movieId]

    # Sorting the DataFrame by the 'cosine_similarity' column in descending order.
    movie_cosines_df = movie_cosines_df.sort_values(by="cosine_similarity", ascending=False)

    # Finding out the number of users who rated both the input movie and the other movie
    no_of_users_rated_both_movies = [
        sum((user_movie_matrix[movieId] > 0) & (user_movie_matrix[other_movieId] > 0))
        for other_movieId in movie_cosines_df.index
    ]

    # Creating a column for the number of users who rated both movies
    movie_cosines_df['users_who_rated_both_movies'] = no_of_users_rated_both_movies

    # Removing recommendations that have less than 20 users who rated both movies.
    movie_cosines_df = movie_cosines_df[movie_cosines_df["users_who_rated_both_movies"] > 20]

    # Getting the titles of the recommended movies
    recommended_movie_titles = movie_ratings_tags.loc[movie_cosines_df.index, "title"]

    # Creating a DataFrame with unique titles
    unique_recommendations = pd.DataFrame({
        'Movie Title': recommended_movie_titles,
        'Cosine Similarity': movie_cosines_df['cosine_similarity'],
        'Users Rated Both Movies': movie_cosines_df['users_who_rated_both_movies']
    }).drop_duplicates(subset='Movie Title')

    # Returning the top 'n' recommendations with unique titles
    top_n_recommendations = unique_recommendations.head(n)

    return top_n_recommendations

# Sample DataFrames (Replace with your actual data)
movies_cosines_matrix = pd.DataFrame()  # Replace with your actual DataFrame
user_movie_matrix = pd.DataFrame()  # Replace with your actual DataFrame
movie_ratings_tags = pd.DataFrame()  # Replace with your actual DataFrame

# Streamlit App
st.title("WBSFlix Recommender")
st.write("The best movie recommendations for you!")

# Input for user's favorite movie
title = st.text_input("What is your favorite movie?")
st.write("Your favorite movie is:", title)

# Call the recommendation function
recommendations = get_top_n_recommendations(movie_title, 5, movies_cosines_matrix, user_movie_matrix, movie_ratings_tags)

# Display the recommendations
st.write("Top 5 Recommendations:")
st.table(recommendations)