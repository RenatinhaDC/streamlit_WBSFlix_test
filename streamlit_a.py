
#Function for streamlit
import streamlit as st
import pandas as pd

# Calculate weighted scores and get top movies
rating_w8t = 0.6
count_w8t = 0.4

rating_count_df['w8ed_score'] = (rating_count_df['mean'] * rating_w8t) + (rating_count_df['count'] * count_w8t)

top_movies = rating_count_df.sort_values(by='w8ed_score', ascending=False).head(20)

top_movies_info = movie_ratings_tags[movie_ratings_tags['movieId'].isin(top_movies['movieId'])][movie_info_columns].drop_duplicates()

top_movies_info = top_movies_info.merge(top_movies[['movieId', 'w8ed_score']], on='movieId', how='left')

# Streamlit App
st.title("Top Movie Recommender")
st.write("Discover top-rated movies!")

# Function to get top recommendations (Input is DataFrame and n)
def get_top_n(top_movies_info, n):
    top_n_movies_df = pd.DataFrame(top_movies_info).nlargest(n, "w8ed_score")
    return top_n_movies_df

# Input for the number of movies to recommend
n_recommendations = st.number_input("How many movies would you like to recommend?", min_value=1, max_value=10, value=3, step=1)

# Display the top recommendations
top_n_recommendations = get_top_n(top_movies_info, n_recommendations)
st.write(f"Top {n_recommendations} Recommendations:")
st.table(top_n_recommendations)