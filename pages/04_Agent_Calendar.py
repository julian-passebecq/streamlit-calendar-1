import streamlit as st
import plotly.graph_objects as go
from utils.genetic_algorithm import Agent, Meeting

st.title("Agent Calendars")

if 'best_schedule' not in st.session_state:
    st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
    st.stop()

best_schedule = st.session_state.best_schedule

# Sidebar for agent selection
st.sidebar.title("Agent Selection")
selected_agent_id = st.sidebar.selectbox("Select Agent", options=[agent.id for agent in best_schedule.agents])

# Get the selected agent's schedule
selected_agent = next(agent for agent in best_schedule.agents if agent.id == selected_agent_id)
agent_meetings = [meeting for meeting, agent in best_schedule.assignments.items() if agent.id == selected_agent_id]

# Create a timeline for the agent
fig = go.Figure()

for meeting in agent_meetings:
    fig.add_trace(go.Bar(
        x=[meeting.start_slot, meeting.start_slot + meeting.duration],
        y=[meeting.required_skill],
        orientation='h',
        name=f"Meeting {meeting.start_slot}"
    ))

fig.update_layout(
    title=f"Schedule for Agent {selected_agent_id}",
    xaxis_title="Time Slot",
    yaxis_title="Meeting Type",
    barmode='stack',
    height=400,
    showlegend=False
)

st.plotly_chart(fig)

# Display agent details
st.subheader(f"Agent {selected_agent_id} Details")
st.write(f"Skills: {', '.join(selected_agent.skills)}")
st.write(f"Total meetings: {len(agent_meetings)}")

# Display meeting details
st.subheader("Meeting Details")
for meeting in agent_meetings:
    st.write(f"Start: {meeting.start_slot}, Duration: {meeting.duration}, Skill: {meeting.required_skill}")