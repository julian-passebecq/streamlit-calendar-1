import streamlit as st
from pages.calendar_page import show_calendar_page
from pages.genetic_algorithm_page import show_genetic_algorithm_page
from pages.results_page import show_results_page

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Calendar", "Genetic Algorithm", "Results"])

    if page == "Calendar":
        show_calendar_page()
    elif page == "Genetic Algorithm":
        show_genetic_algorithm_page()
    elif page == "Results":
        show_results_page()

if __name__ == "__main__":
    main()
