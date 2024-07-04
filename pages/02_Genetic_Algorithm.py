import streamlit as st
import random
from utils.genetic_algorithm import Agent, Meeting, genetic_algorithm, fitness

st.title("Genetic Algorithm Scheduling")

# Sidebar for genetic algorithm settings
st.sidebar.title("Genetic Algorithm Settings")
num_agents = st.sidebar.number_input("Number of Agents", min_value=1, max_value=10, value=5)
num_meetings = st.sidebar.number_input("Number of Meetings", min_value=1, max_value=50, value=20)

# Function to generate agents based on user input
def generate_agents(num_agents):
    skills = ["Fire", "Security", "Maintenance"]
    agents = []
    for i in range(num_agents):
        agent_skills = random.sample(skills, random.randint(1, len(skills)))
        agents.append(Agent(i, agent_skills))
    return agents

# Generate agents
agents = generate_agents(num_agents)

st.subheader("Agent Skills")
for agent in agents:
    st.write(f"Agent {agent.id}: {', '.join(agent.skills)}")

# Generate meetings
meetings = [
    Meeting(
        start_slot=random.randint(0, 47),
        duration=random.randint(1, 4),
        required_skill=random.choice(["Fire", "Security", "Maintenance", "Monitoring"])
    )
    for _ in range(num_meetings)
]

# Genetic Algorithm Parameters
st.subheader("Genetic Algorithm Parameters")
pop_size = st.number_input("Population Size", min_value=10, max_value=1000, value=50)
generations = st.number_input("Number of Generations", min_value=10, max_value=1000, value=100)
mutation_rate = st.slider("Mutation Rate", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

# Run genetic algorithm
if st.button("Run Genetic Algorithm"):
    progress_bar = st.progress(0)
    best_fitness_history = []
    avg_fitness_history = []

    for i in range(generations):
        best_schedule = genetic_algorithm(agents, meetings, pop_size, 1, mutation_rate)
        best_fitness = fitness(best_schedule)
        avg_fitness = best_fitness  # Since we're only getting one schedule per generation

        best_fitness_history.append(best_fitness)
        avg_fitness_history.append(avg_fitness)

        progress_bar.progress((i + 1) / generations)

    st.session_state.best_schedule = best_schedule
    st.session_state.best_fitness_history = best_fitness_history
    st.session_state.avg_fitness_history = avg_fitness_history

    st.success("Genetic algorithm completed. View results in the Results page.")