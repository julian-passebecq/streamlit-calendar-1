import streamlit as st
from utils.genetic_algorithm import genetic_algorithm, Agent, Meeting

def show():
    st.title("Genetic Algorithm Scheduling")
    
    # Input for number of agents
    num_agents = st.number_input("Number of Agents", min_value=1, max_value=10, value=5)
    
    # Input for agent skills
    st.subheader("Agent Skills")
    agents = []
    for i in range(num_agents):
        skills = st.multiselect(f"Agent {i+1} Skills", ["Fire", "Security", "Maintenance"], key=f"agent_{i}")
        agents.append(Agent(i, skills))
    
    # Input for meetings
    st.subheader("Meetings")
    num_meetings = st.number_input("Number of Meetings", min_value=1, max_value=50, value=20)
    meetings = []
    for i in range(num_meetings):
        col1, col2, col3 = st.columns(3)
        with col1:
            start_slot = st.number_input(f"Meeting {i+1} Start Slot", min_value=0, max_value=47, value=0, key=f"start_{i}")
        with col2:
            duration = st.number_input(f"Meeting {i+1} Duration", min_value=1, max_value=4, value=1, key=f"duration_{i}")
        with col3:
            required_skill = st.selectbox(f"Meeting {i+1} Required Skill", ["Fire", "Security", "Maintenance", "Monitoring"], key=f"skill_{i}")
        meetings.append(Meeting(start_slot, duration, required_skill))
    
    # Run genetic algorithm
    if st.button("Run Genetic Algorithm"):
        best_schedule = genetic_algorithm(agents, meetings, pop_size=50, generations=100, mutation_rate=0.1)
        st.session_state.best_schedule = best_schedule
        st.success("Genetic algorithm completed. View results in the Results page.")