import streamlit as st
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('data.db')

def load_data():
    conn = get_connection()
    query = "SELECT * FROM movies"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(page_title="Movie Database", layout="wide")
    st.title("🎬 Movie Database Viewer")

    st.markdown("""
    This app displays movie data scraped from [SSR1 Scrape Center](https://ssr1.scrape.center/) 
    and stored in a SQLite database.
    """)

    try:
        df = load_data()
        
        # Sidebar filters
        st.sidebar.header("Filters")
        
        # Search by Title
        search_term = st.sidebar.text_input("Search by Title", "")
        
        # Filter by Score
        min_score = st.sidebar.slider("Minimum Score", 0.0, 10.0, 0.0, 0.1)
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]
            
        # Convert score to numeric for filtering, handling potential non-numeric values gracefully
        filtered_df['score_numeric'] = pd.to_numeric(filtered_df['score'], errors='coerce')
        filtered_df = filtered_df[filtered_df['score_numeric'] >= min_score]
        filtered_df = filtered_df.drop(columns=['score_numeric'])

        st.subheader(f"Total Movies: {len(filtered_df)}")
        
        # Display Data
        st.dataframe(filtered_df, use_container_width=True)

        # Download Button
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_movies.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure 'data.db' exists in the current directory.")

if __name__ == "__main__":
    main()
