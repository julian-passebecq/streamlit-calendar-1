import streamlit as st
import random
from utils.genetic_algorithm import Agent
import plotly.graph_objects as go
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

    # Calculate and display workload information
    st.subheader("Workload Information")

    # Weekly workload
    full_time_hours = st.session_state.full_time_agents * 40  # 40 hours per week for full-time
    part_time_hours = st.session_state.part_time_agents * 32  # 32 hours per week for part-time (80%)
    total_weekly_hours = full_time_hours + part_time_hours

    st.write(f"Total Weekly Hours: {total_weekly_hours}")
    st.write(f"Average Daily Hours: {total_weekly_hours / 5:.2f}")  # Assuming 5 working days

    # Create a DataFrame for daily workload
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    daily_workload = [total_weekly_hours / 5] * 5  # Evenly distribute hours across 5 days

    df = pd.DataFrame({
        'Day': days,
        'Hours': daily_workload
    })

    # Create a bar chart for daily workload
    fig = go.Figure(data=[go.Bar(x=df['Day'], y=df['Hours'])])
    fig.update_layout(title='Daily Workload Distribution',
                      xaxis_title='Day of Week',
                      yaxis_title='Working Hours')
    st.plotly_chart(fig)

    # Pie chart for agent type distribution
    labels = ['Full-time', 'Part-time']
    values = [st.session_state.full_time_agents, st.session_state.part_time_agents]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Agent Type Distribution')
    st.plotly_chart(fig)

    # Bar chart for skill distribution
    skills = ['Fire', 'Security', 'Maintenance', 'Monitoring']
    skill_counts = [fire_agents, security_agents, maintenance_agents, num_agents - max(fire_agents, security_agents, maintenance_agents)]

    fig = go.Figure(data=[go.Bar(x=skills, y=skill_counts)])
    fig.update_layout(title='Skill Distribution',
                      xaxis_title='Skill',
                      yaxis_title='Number of Agents')
    st.plotly_chart(fig)

else:
    st.warning("No agent configuration saved yet. Please configure and save agents.")