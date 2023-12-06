import numpy as np
import pandas as pd
import pywhatkit as pwt
import streamlit as st

# Load data (assuming the pickle files are available)
pt = pd.read_pickle('pt1.pkl')
books = pd.read_pickle('books.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')
popular1 = pd.read_pickle('popular1.pkl')
final = pd.read_pickle('final_ratings.pkl')

pt1 = pd.DataFrame(pt)
final_ratings = pd.DataFrame(final)
popular = pd.DataFrame(popular1)


def search(search_str):
    search_str = search_str + " :- book"
    return pwt.search(search_str)


def recommend(book_name):
    print("Recommended Books:")

    index = np.where(pt1.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:10]

    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt1.index[i[0]]]
        url = temp_df['Image-URL-L'].values[0]
        title = temp_df['Book-Title'].values[0]
        author = temp_df['Book-Author'].values[0]
        year = temp_df['Year-Of-Publication'].values[0]
        
        print(f"Book Title: {title}")
        print(f"Author Name: {author}")
        print(f"Year Of Publication: {year}")
        # Add other information or processing here


def show_popular():
    print("Top 50 Popular Books:")

    for i in range(len(popular1)):
        title = popular1.iloc[i]['Book-Title']
        author = popular1.iloc[i]['Book-Author']
        avg = popular1.iloc[i]['avg-rating']
        
        print(f"Book Title: {title}")
        print(f"Book Author: {author}")
        print(f"Rating: {avg}")
        # Add other information or processing here


selected = "Recommend"  # Change this to simulate different selections

if selected == "Home":
    show_popular()

if selected == "Recommend":
    book_titles = pt1.index.tolist()
    selected_book = "Your Selected Book"  # Replace this with a book title for testing
    recommend(selected_book)
