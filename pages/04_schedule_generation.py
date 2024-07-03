import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import the generate_and_optimize_schedule function from the genetic algorithm module
from src.genetic_algorithm import generate_and_optimize_schedule

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
    col1, col2 = st.columns(2)
    
    with col1:
        population_size = st.number_input("Population Size", min_value=10, max_value=1000, value=100)
        generations = st.number_input("Number of Generations", min_value=10, max_value=1000, value=100)
    
    with col2:
        mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.1, step=0.01)
        crossover_rate = st.slider("Crossover Rate", min_value=0.0, max_value=1.0, value=0.8, step=0.01)

    if st.button("Generate Schedule"):
        with st.spinner("Generating schedule..."):
            optimized_schedule = generate_and_optimize_schedule(
                st.session_state.agents, 
                st.session_state.missions, 
                population_size, 
                generations, 
                mutation_rate, 
                crossover_rate
            )
        
        st.success("Schedule generated successfully!")
        
        # Display the generated schedule
        st.subheader("Generated Schedule")
        for agent, missions in optimized_schedule.items():
            st.write(f"Agent {agent}:")
            for mission in missions:
                st.write(f"- {mission['Client']} ({mission['Type']}): {mission['Start Time']} - {mission['Duration']} hours")
            st.write("---")

schedule_generation_page()