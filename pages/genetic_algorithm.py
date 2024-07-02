import streamlit as st
from utils.scheduling_utils import genetic_algorithm, Agent
from utils.meeting_utils import meeting_types

def show():
    st.title("Genetic Algorithm Scheduling")

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

    if st.button("Run Genetic Algorithm"):
        meetings = st.session_state.calendar_events
        agents = st.session_state.agents

        progress_bar = st.progress(0)
        status_text = st.empty()

        def progress_callback(generation, best_fitness):
            progress = generation / num_generations
            progress_bar.progress(progress)
            status_text.text(f"Generation: {generation}/{num_generations}, Best Fitness: {best_fitness:.2f}")

        best_schedule = genetic_algorithm(agents, meetings, population_size, num_generations, mutation_rate, progress_callback)
        st.session_state.best_schedule = best_schedule
        st.success("Scheduling completed. View results in the Results page.")

    st.subheader("Algorithm Explanation")
    st.write("""
    The genetic algorithm works as follows:
    1. Initialize a population of random schedules.
    2. Evaluate the fitness of each schedule based on constraints and objectives.
    3. Select the best schedules to be parents for the next generation.
    4. Create new schedules through crossover of parent schedules.
    5. Introduce random mutations to maintain diversity.
    6. Repeat steps 2-5 for the specified number of generations.
    7. Return the best schedule found.
    """)

    st.subheader("Constraints and Objectives")
    st.write("""
    - Agents must have the required skills for their assigned meetings.
    - Avoid overlapping meetings for the same agent.
    - Maintain at least 30 minutes between an agent's meetings.
    - Limit shift durations to 8 hours when possible.
    - Ensure all meetings are assigned to an agent.
    """)

    st.subheader("Meeting Types and Required Skills")
    for meeting_type, info in meeting_types.items():
        st.write(f"{meeting_type}: {info['duration']} hour(s)")