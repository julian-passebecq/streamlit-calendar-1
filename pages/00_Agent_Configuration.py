import streamlit as st
import random
from utils.genetic_algorithm import Agent
import pandas as pd

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
skill_pool = ['Fire'] * fire_agents + ['Security'] * security_agents + ['Maintenance'] * maintenance_agents
random.shuffle(skill_pool)

for i in range(num_agents):
    skills = set()
    while len(skills) < 2 and skill_pool:
        skill = skill_pool.pop()
        skills.add(skill)
    skills.add("Monitoring")  # All agents can do monitoring
    agents.append(Agent(i, list(skills)))

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

    # Calculate workload information
    st.subheader("Workload Information")

    # Weekly workload
    full_time_hours = st.session_state.full_time_agents * 40  # 40 hours per week for full-time
    part_time_hours = st.session_state.part_time_agents * 32  # 32 hours per week for part-time (80%)
    total_weekly_hours = full_time_hours + part_time_hours

    st.write(f"Total Weekly Hours: {total_weekly_hours}")
    st.write(f"Average Daily Hours: {total_weekly_hours / 5:.2f}")  # Assuming 5 working days

    # Calculate workload distribution by skill
    skill_hours = {
        'Fire': fire_agents * 40,
        'Security': security_agents * 40,
        'Maintenance': maintenance_agents * 40,
        'Monitoring': total_weekly_hours  # All agents can do monitoring
    }

    # Create a DataFrame for weekly workload by skill
    df_weekly = pd.DataFrame({
        'Skill': skill_hours.keys(),
        'Weekly Hours': skill_hours.values()
    })

    st.subheader("Weekly Workload by Skill")
    st.table(df_weekly)

    # Create a DataFrame for daily workload by skill
    df_daily = pd.DataFrame({
        'Skill': skill_hours.keys(),
        'Daily Hours': [hours / 5 for hours in skill_hours.values()]
    })

    st.subheader("Daily Workload by Skill")
    st.table(df_daily)

else:
    st.warning("No agent configuration saved yet. Please configure and save agents.")

# Additional ideas
st.subheader("Additional Information")
st.write("1. Skill Overlap: Some agents have multiple skills, which allows for flexible scheduling.")
st.write("2. Monitoring Capacity: All agents can perform monitoring tasks, providing a baseline workload distribution.")
st.write("3. Part-time Impact: Part-time agents (if any) contribute 80% of full-time hours, affecting overall capacity.")
st.write("4. Peak Hours: Consider that certain skills might be in higher demand during specific times of day.")
st.write("5. Training Needs: Agents with fewer skills might benefit from cross-training to increase scheduling flexibility.")