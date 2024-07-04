import streamlit as st
import random
from utils.genetic_algorithm import Agent

st.title("Agent Configuration")

# Sidebar for agent settings
st.sidebar.title("Agent Settings")
num_agents = st.sidebar.number_input("Number of Agents", min_value=1, max_value=20, value=5)

# Main content
st.write(f"Configure {num_agents} agents:")

agents = []
for i in range(num_agents):
    st.subheader(f"Agent {i+1}")
    skills = st.multiselect(
        f"Select skills for Agent {i+1}",
        options=["Fire", "Security", "Maintenance"],
        default=random.sample(["Fire", "Security", "Maintenance"], k=1)
    )
    agents.append(Agent(i, skills))

if st.button("Save Agent Configuration"):
    st.session_state.agents = agents
    st.success("Agent configuration saved!")

# Display current agent configuration
if 'agents' in st.session_state:
    st.subheader("Current Agent Configuration")
    for agent in st.session_state.agents:
        st.write(f"Agent {agent.id}: {', '.join(agent.skills)}")