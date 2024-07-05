import streamlit as st
import plotly.graph_objects as go
from utils.genetic_algorithm import fitness

st.title("Scheduling Results")

if 'best_schedule' not in st.session_state:
    st.warning("No schedule has been generated yet. Please run the genetic algorithm first.")
else:
    best_schedule = st.session_state.best_schedule
    best_fitness_history = st.session_state.best_fitness_history
    avg_fitness_history = st.session_state.avg_fitness_history

    # Retrieve penalty values from session state or use default values
    penalty_wrong_skill = st.session_state.get('penalty_wrong_skill', 100)
    penalty_overlap = st.session_state.get('penalty_overlap', 50)
    penalty_consecutive = st.session_state.get('penalty_consecutive', 25)
    penalty_overwork = st.session_state.get('penalty_overwork', 10)
    penalty_long_shift = st.session_state.get('penalty_long_shift', 50)

    st.subheader("Best Schedule")
    st.write(f"Fitness Score: {fitness(best_schedule, penalty_wrong_skill, penalty_overlap, penalty_consecutive, penalty_overwork, penalty_long_shift)}")

    for meeting, agent in best_schedule.assignments.items():
        st.write(
            f"Meeting (Start: {meeting.start.strftime('%Y-%m-%d %H:%M')}, Duration: {meeting.duration} hours, Skill: {meeting.required_skill}) assigned to Agent {agent.id}")

    # Fitness History Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=best_fitness_history, mode='lines', name='Best Fitness'))
    fig.add_trace(go.Scatter(y=avg_fitness_history, mode='lines', name='Average Fitness'))
    fig.update_layout(title='Fitness History', xaxis_title='Generation', yaxis_title='Fitness Score')
    st.plotly_chart(fig)

    # Agent Workload
    agent_workload = {agent.id: 0 for agent in best_schedule.agents}
    for meeting, agent in best_schedule.assignments.items():
        agent_workload[agent.id] += meeting.duration

    fig = go.Figure(data=[go.Bar(x=list(agent_workload.keys()), y=list(agent_workload.values()))])
    fig.update_layout(title='Agent Workload', xaxis_title='Agent ID', yaxis_title='Total Hours')
    st.plotly_chart(fig)

    # Sidebar for result analysis
    st.sidebar.title("Result Analysis")
    selected_agent = st.sidebar.selectbox("Select Agent for Detailed View", options=[agent.id for agent in best_schedule.agents])

    st.subheader(f"Detailed Schedule for Agent {selected_agent}")
    agent_meetings = [meeting for meeting, agent in best_schedule.assignments.items() if agent.id == selected_agent]
    agent_meetings.sort(key=lambda x: x.start)

    for meeting in agent_meetings:
        st.write(f"Start: {meeting.start.strftime('%Y-%m-%d %H:%M')}, Duration: {meeting.duration} hours, Skill: {meeting.required_skill}")

    # Add more analysis options here as needed