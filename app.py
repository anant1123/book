
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from googlesearch import search as google_search

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
    results = google_search(search_str, num=1, stop=1)
    return list(results)


def recommend(book_name):
    st.subheader("Recommended Books")

    index = np.where(pt1.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:10]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt1.index[i[0]]]

        # Check if temp_df is not empty before accessing its elements
        if not temp_df.empty:
            url = temp_df['Image-URL-L'].values[0]
            title = temp_df['Book-Title'].values[0]
            author = temp_df['Book-Author'].values[0]
            year = temp_df['Year-Of-Publication'].values[0]
            data.append((url, title, author, year))

    num_items = len(data)
    num_cols = 3
    num_rows = int(np.ceil(num_items / num_cols))

    col1, col2, col3 = st.columns(num_cols)

    for i, item in enumerate(data):
        col_idx = i % num_cols
        row_idx = i // num_cols
        with col1 if col_idx == 0 else col2 if col_idx == 1 else col3:
            st.image(item[0], width=150)
            st.markdown(f"**Book Title:** {item[1]}")
            st.markdown(f"**Author Name:** {item[2]}")
            st.markdown(f"**Year Of Publication:** {item[3]}")


def show_popular():

    st.title("Top 50 Popular Books")

    data = []
    for i in range(len(popular1)):

        title = popular1.iloc[i]['Book-Title']
        author = popular1.iloc[i]['Book-Author']
        url = popular1.iloc[i]['Image-URL-L']
        avg = popular1.iloc[i]['avg-rating']
        data.append((title, author, url, avg))


    num_items = len(data)
    num_cols = 3
    col_width = 200
    num_rows = int(np.ceil(num_items / num_cols))

    col1, col2, col3 = st.columns(num_cols)

    for i, item in enumerate(data):
        col_idx = i % num_cols
        row_idx = i // num_cols
        with col1 if col_idx == 0 else col2 if col_idx == 1 else col3:
            st.image(item[2])
            st.markdown(f"**Book Title:** {item[0]}")
            st.markdown(f"**Book Author:** {item[1]}")
            st.markdown(f"**Rating:** {item[3]}")

            img = item[2]

            btn = st.button("Google Link", img)

            if btn:
                search(item[0])



with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Recommend"],
        icons=["house", "book"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Home":
    show_popular()

if selected == "Recommend":
    st.title("Book Recommender System")
    book_titles = pt1.index.tolist()
    selected_book = st.selectbox(f"Select Book Name", book_titles)
    col1, col2 = st.columns(2)

    if col1.button('recommend'):
        recommend(selected_book)

def app():
    st.title("Book-Recommendation")

if __name__ == "__main__":
    app()
