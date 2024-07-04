import streamlit as st
import random
import plotly.graph_objects as go
from utils.genetic_algorithm import Agent, Meeting, genetic_algorithm, fitness, initialize_population

st.title("Genetic Algorithm Scheduling")

# Check if agents are configured
if 'agents' not in st.session_state:
    st.warning("Please configure agents in the Agent Configuration page first.")
    st.stop()

if 'calendar_events' not in st.session_state:
    st.warning("Please generate a calendar in the Calendar page first.")
    st.stop()

agents = st.session_state.agents
calendar_events = st.session_state.calendar_events

# Convert calendar events to meetings
meetings = [
    Meeting(
        start_slot=int(event['start'].split('T')[1].split(':')[0]) * 2 + (1 if event['start'].split('T')[1].split(':')[1] == '30' else 0),
        duration=int((datetime.datetime.fromisoformat(event['end']) - datetime.datetime.fromisoformat(event['start'])).total_seconds() / 1800),
        required_skill=event['type']
    )
    for event in calendar_events
]

# Genetic Algorithm Parameters
st.subheader("Genetic Algorithm Parameters")
pop_size = st.number_input("Population Size", min_value=10, max_value=1000, value=50)
generations = st.number_input("Number of Generations", min_value=10, max_value=1000, value=100)
mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

# Penalty values
st.subheader("Penalty Values")
penalty_wrong_skill = st.number_input("Wrong Skill Penalty", value=100, step=10)
penalty_overlap = st.number_input("Overlapping Meetings Penalty", value=50, step=10)
penalty_consecutive = st.number_input("Consecutive Meetings Penalty", value=25, step=5)
penalty_overwork = st.number_input("Overwork Penalty (per slot)", value=10, step=1)
penalty_long_shift = st.number_input("Long Shift Penalty", value=50, step=10)

# Run genetic algorithm
if st.button("Run Genetic Algorithm"):
    progress_bar = st.progress(0)
    best_fitness_history = []
    avg_fitness_history = []
    population = initialize_population(pop_size, agents, meetings)

    for i in range(generations):
        best_schedule = genetic_algorithm(agents, meetings, pop_size, 1, mutation_rate,
                                          penalty_wrong_skill, penalty_overlap, penalty_consecutive,
                                          penalty_overwork, penalty_long_shift)
        population_fitness = [fitness(schedule, penalty_wrong_skill, penalty_overlap, penalty_consecutive,
                                      penalty_overwork, penalty_long_shift) for schedule in population]
        best_fitness = max(population_fitness)
        avg_fitness = sum(population_fitness) / len(population_fitness)

        best_fitness_history.append(best_fitness)
        avg_fitness_history.append(avg_fitness)

        progress_bar.progress((i + 1) / generations)

    st.session_state.best_schedule