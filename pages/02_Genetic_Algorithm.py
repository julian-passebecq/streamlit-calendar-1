import streamlit as st
import random
import plotly.graph_objects as go
from utils.genetic_algorithm import Agent, Meeting, genetic_algorithm, fitness, initialize_population

st.title("Genetic Algorithm Scheduling")

# Check if agents are configured
if 'agents' not in st.session_state:
    st.warning("Please configure agents in the Agent Configuration page first.")
    st.stop()

agents = st.session_state.agents

# Sidebar for genetic algorithm settings
st.sidebar.title("Genetic Algorithm Settings")
num_meetings = st.sidebar.number_input("Number of Meetings", min_value=1, max_value=50, value=20)

# Generate meetings based on agent capacity and skills
total_capacity = len(agents) * 5  # Assuming 5 hours of meetings per agent per day
meetings = []
for _ in range(min(num_meetings, total_capacity)):
    required_skill = random.choice(["Fire", "Security", "Maintenance", "Monitoring"])
    start_slot = random.randint(0, 47)
    duration = random.randint(1, 4)
    meetings.append(Meeting(start_slot, duration, required_skill))

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

    st.session_state.best_schedule = best_schedule
    st.session_state.best_fitness_history = best_fitness_history
    st.session_state.avg_fitness_history = avg_fitness_history

    # Visualize genetic algorithm process
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=best_fitness_history, mode='lines', name='Best Fitness'))
    fig.add_trace(go.Scatter(y=avg_fitness_history, mode='lines', name='Average Fitness'))
    fig.update_layout(title='Fitness History', xaxis_title='Generation', yaxis_title='Fitness Score')
    st.plotly_chart(fig)

    st.success("Genetic algorithm completed. View results in the Results page.")

# Visualize chromosome
if 'best_schedule' in st.session_state:
    st.subheader("Best Schedule Chromosome")
    chromosome = []
    for meeting in meetings:
        agent = st.session_state.best_schedule.assignments.get(meeting, None)
        chromosome.append(agent.id if agent else -1)
    
    fig = go.Figure(data=[go.Bar(y=chromosome, x=[f"M{i}" for i in range(len(chromosome))])])
    fig.update_layout(title='Chromosome Representation', xaxis_title='Meetings', yaxis_title='Agent ID')
    st.plotly_chart(fig)