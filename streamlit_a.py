import streamlit as st

st.title("WBSFlix Recomender")

st.write("The best movie recomendations for you!")

title= st.text_input("What is your favourite movie")

st.write("Your favourite movie is:", title)


import streamlit as st
import pandas as pd

# Assuming your function is defined here
def get_top_n_recommendations(movieId, n, movies_cosines_matrix, user_movie_matrix, movie_ratings_tags):
    # ... (your function implementation)

# Load your data or perform any necessary setup
# ...

# Streamlit App
st.title("WBSFlix Recommender")

# Sidebar for user input
title = st.sidebar.text_input("What is your favorite movie", "Toy Story (1995)")

# Main area to display recommendations
st.header("Your Recommendations")

# Display user's favorite movie
st.write("Your favorite movie is:", title)

# Add a button to trigger the recommendation process
if st.button("Get Recommendations"):
    # Assuming you have the necessary data loaded
    # Replace the following lines with your actual data
    movies_cosines_matrix = pd.DataFrame()
    user_movie_matrix = pd.DataFrame()
    movie_ratings_tags = pd.DataFrame()

    # Call your recommendation function
    recommendations = get_top_n_recommendations(
        movieId=your_movie_id,
        n=your_top_n_value,
        movies_cosines_matrix=movies_cosines_matrix,
        user_movie_matrix=user_movie_matrix,
        movie_ratings_tags=movie_ratings_tags
    )

    # Display the recommendations
    st.write("Top Recommendations:")
    st.table(recommendations)