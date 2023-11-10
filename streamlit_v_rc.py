import pandas as pd
import streamlit as st

movie_ratings_tags = pd.read_csv("movie_ratings_tags.csv") 

#links= pd.read_csv("links.csv")

movies= pd.read_csv("movies.csv")

ratings= pd.read_csv("ratings.csv")

tags= pd.read_csv("tags.csv")

# Merging movies and ratings on 'movieId'
movie_ratings = pd.merge(movies, ratings, on='movieId')

# Merging movie_ratings and tags on 'movieId'
movie_ratings_tags = pd.merge(movie_ratings, tags, on='movieId')


becouse_you_like = st.container()

with becouse_you_like:
    st.header('Similar to')
    #st.text('Write a name')
    #title = st.text_input("What is your favorite movie?")
    #st.write("Your favorite movie is:", title)
    
    #selection_col, display_col = st.columns(2)
    input_feature = str(st.text_input('Movie title'))
    st.write("Your favorite movie is:", input_feature)
    
    # py function get sparse matrix
    def get_sparse_matrix(data: pd.DataFrame): 

         return(movie_ratings_tags.pivot_table(data=movie_ratings_tags,
                                  values='rating',
                                  index='userId_x',
                                  columns='title',
                                  fill_value=0)            
         )



    # py function item based recommender
    def item_based_recommender(data: pd.DataFrame, title: str, n: int=5):
    
        sparse_matrix = get_sparse_matrix(movie_ratings_tags)
        
        return(
             sparse_matrix
                 .corrwith(sparse_matrix[title])
                 .sort_values(ascending=False)
                 .index
                 .to_list()[1:n+1]
             )
    similar_movies = item_based_recommender(movie_ratings_tags, input_feature)
    
    

    #st.dataframe(similar_movies)