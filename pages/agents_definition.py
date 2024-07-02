import streamlit as st
from utils.scheduling_utils import Agent

def show():
    st.title("Agent Definition")

    if 'agents' not in st.session_state:
        st.session_state.agents = []

    num_agents = st.number_input("Number of Agents", min_value=1, max_value=20, value=5)

    for i in range(num_agents):
        st.subheader(f"Agent {i+1}")
        name = st.text_input(f"Name for Agent {i+1}", value=f"Agent {i+1}")
        skills = st.multiselect(f"Skills for Agent {i+1}", ["Fire", "Security", "Maintenance", "Monitoring"])
        
        if i < len(st.session_state.agents):
            st.session_state.agents[i] = Agent(i, name, skills)
        else:
            st.session_state.agents.append(Agent(i, name, skills))

    if st.button("Save Agents"):
        st.success(f"Saved {len(st.session_state.agents)} agents.")

    if st.session_state.agents:
        st.subheader("Defined Agents")
        for agent in st.session_state.agents:
            st.write(f"{agent.name}: {', '.join(agent.skills)}")