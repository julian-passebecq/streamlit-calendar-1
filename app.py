import streamlit as st
from pages import calendar_page, genetic_algorithm_page, results_page

st.set_page_config(page_title="Scheduling App", layout="wide")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Calendar", "Genetic Algorithm", "Results"])

    if page == "Calendar":
        calendar_page.show()
    elif page == "Genetic Algorithm":
        genetic_algorithm_page.show()
    elif page == "Results":
        results_page.show()

if __name__ == "__main__":
    main()