import streamlit as st
from utils.scheduling_utils import genetic_algorithm

def show():
    st.title("Scheduling")

    if 'calendar_events' not in st.session_state:
        st.warning("Please generate meetings first in the Meeting Generation page.")
        return

    if 'agents' not in st.session_state or not st.session_state.agents:
        st.warning("Please define agents first in the Agent Definition page.")
        return

    st.subheader("Genetic Algorithm Parameters")
    population_size = st.slider("Population Size", 10, 200, 50)
    num_generations = st.slider("Number of Generations", 10, 1000, 100)
    mutation_rate = st.slider("Mutation Rate", 0.0, 1.0, 0.1)

    if st.button("Run Scheduling Algorithm"):
        meetings = [event for event in st.session_state.calendar_events]
        agents = st.session_state.agents

        best_schedule = genetic_algorithm(agents, meetings, population_size, num_generations, mutation_rate)
        st.session_state.best_schedule = best_schedule
        st.success("Scheduling completed. View results in the Results page.")