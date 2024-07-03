import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import the generate_and_optimize_schedule function from the genetic algorithm artifact
from genetic_algorithm import generate_and_optimize_schedule

def schedule_generation_page():
    st.header("Schedule Generation")

    # Check if we have agents and missions data
    if 'agents' not in st.session_state or 'missions' not in st.session_state:
        st.warning("Please add agents and missions before generating a schedule.")
        return

    if st.session_state.agents.empty or st.session_state.missions.empty:
        st.warning("Please add at least one agent and one mission before generating a schedule.")
        return

    # Display current agents and missions
    st.subheader("Current Agents")
    st.dataframe(st.session_state.agents)

    st.subheader("Current Missions")
    st.dataframe(st.session_state.missions)

    # Genetic Algorithm Parameters
    st.subheader("Genetic Algorithm Parameters")
    col1, col2 = st.columns(