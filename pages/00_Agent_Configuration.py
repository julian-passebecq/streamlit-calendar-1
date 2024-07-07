import streamlit as st
import random
from utils.genetic_algorithm import Agent

st.title("Agent Configuration")

# Sidebar for agent settings
st.sidebar.title("Agent Settings")
num_agents = st.sidebar.number_input("Total Number of Agents", min_value=1, max_value=20, value=5)

# Agent type distribution
st.sidebar.subheader("Agent Type Distribution")
full_time_agents = st.sidebar.number_input("Full-time Agents", min_value=0, max_value=num_agents, value=num_agents)
part_time_agents = num_agents - full_time_agents
st.sidebar.write(f"Part-time Agents (80%): {part_time_agents}")

# Skill distribution
st.sidebar.subheader("Skill Distribution")
fire_agents = st.sidebar.number_input("Agents with Fire skill", min_value=0, max_value=num_agents, value=2)
security_agents = st.sidebar.number_input("Agents with Security skill", min_value=0, max_value=num_agents, value=2)
maintenance_agents = st.sidebar.number_input("Agents with Maintenance skill", min_value=0, max_value=num_agents, value=1)

# Main content
st.write(f"Configuring {num_agents} agents:")

agents = []
for i in range(num_agents):
    skills = []
    if i < fire_agents:
        skills.append("Fire")
    if i < security_agents:
        skills.append("Security")
    if i < maintenance_agents:
        skills.append("Maintenance")
    
    if not skills:
        skills = ["Monitoring"]
    
    agents.append(Agent(i, skills))

if st.button("Save Agent Configuration"):
    st.session_state.agents = agents
    st.session_state.full_time_agents = full_time_agents
    st.session_state.part_time_agents = part_time_agents
    st.success("Agent configuration saved!")

# Display current agent configuration
if 'agents' in st.session_state:
    st.subheader("Current Agent Configuration")
    for agent in st.session_state.agents:
        st.write(f"Agent {agent.id}: {', '.join(agent.skills)}")
    
    st.write(f"Full-time Agents: {st.session_state.full_time_agents}")
    st.write(f"Part-time Agents (80%): {st.session_state.part_time_agents}")