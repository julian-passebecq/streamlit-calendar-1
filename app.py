import streamlit as st
from pages import meeting_generation, agent_definition, genetic_algorithm, results

st.set_page_config(page_title="Security Scheduling App", layout="wide")

PAGES = {
    "Meeting Generation": meeting_generation,
    "Agent Definition": agent_definition,
    "Genetic Algorithm": genetic_algorithm,
    "Results": results
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.show()

if __name__ == "__main__":
    main()