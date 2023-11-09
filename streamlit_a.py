# Import necessary libraries
import streamlit as st
import pandas as pd

# Defining the recommendation function

def get_top_n_recommendations(movie_title, n, movies_cosines_matrix, user_movie_matrix, movie_ratings_tags):
    # Finding the movieId for the given movie title
    movieId = movie_ratings_tags[movie_ratings_tags['title'].str.contains(movie_title, case=False)]['movieId'].values[0]

    # Geting the index corresponding to the movieId
    movie_index = movies_cosines_matrix.index.get_loc(movieId)

    # Creating a DataFrame using the values from 'movies_cosines_matrix' for the input 'movieId'
    movie_cosines_df = pd.DataFrame(movies_cosines_matrix.iloc[movie_index])

    # Renaming the column to 'cosine_similarity'
    movie_cosines_df = movie_cosines_df.rename(columns={movieId: 'cosine_similarity'})

    # Remove the row with the index 'movieId'
    movie_cosines_df = movie_cosines_df[movie_cosines_df.index != movieId]

    # Sorting the DataFrame by the 'cosine_similarity' column in descending order
    movie_cosines_df = movie_cosines_df.sort_values(by="cosine_similarity", ascending=False)

    # Finding out the number of users who rated both the input movie and the other movie
    no_of_users_rated_both_movies = [
        sum((user_movie_matrix[movieId] > 0) & (user_movie_matrix[other_movieId] > 0))
        for other_movieId in movie_cosines_df.index
    ]

    # Creating a column for the number of users who rated both movies
    movie_cosines_df['users_who_rated_both_movies'] = no_of_users_rated_both_movies

    # Removing recommendations that have less than 20 users who rated both movies
    movie_cosines_df = movie_cosines_df[movie_cosines_df["users_who_rated_both_movies"] > 20]

    # Geting the titles of the recommended movies
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

# my data
movies_cosines_matrix = pd.DataFrame()
user_movie_matrix = pd.DataFrame()
movie_ratings_tags = pd.DataFrame()

# Streamlit App
st.title("WBSFlix Recommender")

# Sidebar for user input
title = st.sidebar.text_input("What is your favorite movie", "Toy Story")

# Main area to display recommendations
st.header("Your Recommendations")

# Display user's favorite movie
st.write("Your favorite movie is:", title)

# Add a button to trigger the recommendation process
if st.button("Get Recommendations"):
    # Debugging: Print the contents of movie_ratings_tags
    st.write("Contents of movie_ratings_tags:")
    st.write(movie_ratings_tags)

    try:
        # Call your recommendation function
        recommendations = get_top_n_recommendations(
            movie_title=title,
            n=5,  # Replace with the desired number of recommendations
            movies_cosines_matrix=movies_cosines_matrix,
            user_movie_matrix=user_movie_matrix,
            movie_ratings_tags=movie_ratings_tags
        )

        # Debugging: Print the recommendations
        st.write("Top Recommendations:")
        st.table(recommendations)

    except Exception as e:
        # Print the exception details for debugging
        st.write(f"Error: {e}")
        st.write("Full exception details:")
        st.write(e)