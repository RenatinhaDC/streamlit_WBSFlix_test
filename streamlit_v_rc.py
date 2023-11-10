import pandas as pd
import streamlit as st

#movie_ratings_tags = pd.read_csv("movie_ratings_tags.csv") 

#becouse_you_like = st.container()

#with becouse_you_like:
    st.header('Similar to')
    st.text('Write a name')
    
    #selection_col, display_col = st.columns(2)
    #input_feature = str(st.text_input('Movie title'))
    
    # py function get sparse matrix
    #def get_sparse_matrix(data: pd.DataFrame): 

        # return(movie_ratings_tags.pivot_table(data=movie_ratings_tags,
         #                         values='rating',
         #                         index='userId_x',
          #                        columns='title',
           #                       fill_value=0)            
         #)



    # py function item based recommender
    #def item_based_recommender(data: pd.DataFrame, title: str, n: int=5):
    
     #   sparse_matrix = get_sparse_matrix(movie_ratings_tags)
        
   #     return(
       #      sparse_matrix
        #         .corrwith(sparse_matrix[title])
         #        .sort_values(ascending=False)
          #       .index
           #      .to_list()[1:n+1]
            # )
    #similar_movies = item_based_recommender(movie_ratings_tags.copy(), input_feature)
    
    

    #st.dataframe(similar_movies)